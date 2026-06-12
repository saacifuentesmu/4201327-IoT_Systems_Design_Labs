#!/usr/bin/env python3
"""SoilSense end-to-end test suite — Lab 8 (Golden Master).

Usage:
    python tools/test_e2e.py <node_a_ipv6> [valve_ipv6]
        [--psk-identity iotlab2024] [--psk-key secretkey123456]

Run it from a laptop OUTSIDE the mesh, using each node's global (OMR)
address from `ipaddr`: every passing test then also re-proves the
Lab 5 OTBR path end to end.

What it checks:
  1. plaintext posture  — is coap://:5683 locked out (Lab 6) or open (Lab 7 bridge)?
  2. DTLS               — CoAPS GET with the PSK works; a wrong key fails the
                          handshake (needs coap-client from libcoap2-bin)
  3. telemetry contract — the CBOR payload carries the Lab 7 keys
  4. valve round-trip   — PUT {"v":1} / GET / PUT {"v":0} (4-byte CBOR map)
  5. invalid inputs     — unknown path -> 4.04, malformed valve payload -> 4.00
  6. stress             — 20 sequential GETs: success ratio + latency stats
  7. burst              — 12 parallel GETs: expects 4.29 from the rate limiter

Exit code 0 if nothing FAILed (WARN/SKIP are allowed).
"""
import argparse
import asyncio
import shutil
import statistics
import subprocess
import sys
import time

import aiocoap
from aiocoap.numbers.codes import Code

try:
    import cbor2
except ImportError:
    cbor2 = None

CODE_TOO_MANY_REQUESTS = 157   # 4.29 = 4*32 + 29 (RFC 8516)
VALVE_OPEN = bytes([0xA1, 0x61, 0x76, 0x01])    # {"v": 1}
VALVE_CLOSE = bytes([0xA1, 0x61, 0x76, 0x00])   # {"v": 0}
TELEMETRY_KEYS = {"rssi", "batt", "up"}

results = []


def record(name, status, detail=""):
    results.append({"name": name, "status": status, "detail": detail})
    print(f"[{status:4}] {name}" + (f" — {detail}" if detail else ""))


async def coap_request(ctx, method, uri, payload=b"", timeout=10.0):
    """One CoAP exchange. Returns (response|None, latency_ms, error_str)."""
    msg = aiocoap.Message(code=method, uri=uri, payload=payload)
    start = time.monotonic()
    try:
        resp = await asyncio.wait_for(ctx.request(msg).response, timeout)
        return resp, (time.monotonic() - start) * 1000, None
    except Exception as e:
        return None, (time.monotonic() - start) * 1000, str(e) or type(e).__name__


def coap_client_dtls(host, psk_id, psk_key, path="/env/temp", timeout=15):
    """CoAPS GET via the libcoap CLI (the Lab 6 client). Returns payload bytes or None."""
    cmd = ["coap-client", "-m", "get", "-u", psk_id, "-k", psk_key,
           "-B", str(timeout), f"coaps://[{host}]:5684{path}"]
    try:
        out = subprocess.run(cmd, capture_output=True, timeout=timeout + 5)
    except subprocess.TimeoutExpired:
        return None
    if out.returncode == 0 and out.stdout:
        return out.stdout
    return None


async def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("node_a", help="global IPv6 of Node A (/env/temp server)")
    ap.add_argument("valve", nargs="?", help="global IPv6 of the SED valve node (optional)")
    ap.add_argument("--psk-identity", default="iotlab2024")
    ap.add_argument("--psk-key", default="secretkey123456")
    args = ap.parse_args()

    ctx = await aiocoap.Context.create_client_context()
    have_coap_client = shutil.which("coap-client") is not None
    env_temp_uri = f"coap://[{args.node_a}]/env/temp"

    print("=== SoilSense e2e suite (Lab 8) ===")
    print(f"Node A: {args.node_a}   Valve: {args.valve or '(not given)'}\n")

    # 1 — plaintext posture (informative either way; ADRs must match the finding)
    resp, lat, _ = await coap_request(ctx, aiocoap.GET, env_temp_uri, timeout=5)
    plain_open = resp is not None and resp.code.is_successful()
    plain_payload = resp.payload if plain_open else None
    if plain_open:
        record("plaintext posture", "WARN",
               f":5683 answers ({lat:.0f} ms) — fine if an ADR documents it (Lab 7 bridge), "
               "otherwise a Lab 6 hardening gap")
    else:
        record("plaintext posture", "PASS", ":5683 locked out (Lab 6 hardening in place)")

    # 2 — DTLS, right and wrong PSK
    dtls_payload = None
    if have_coap_client:
        dtls_payload = coap_client_dtls(args.node_a, args.psk_identity, args.psk_key)
        record("DTLS with PSK", "PASS" if dtls_payload else "FAIL",
               "" if dtls_payload else "CoAPS GET returned nothing — check PSK and :5684")
        wrong = coap_client_dtls(args.node_a, args.psk_identity, "definitely-wrong-key")
        record("DTLS wrong-PSK rejected", "PASS" if wrong is None else "FAIL",
               "" if wrong is None else "a wrong key got a response — PSK check broken")
    else:
        record("DTLS tests", "SKIP", "coap-client not found (apt install libcoap2-bin)")

    # 3 — telemetry contract (Lab 7 keys in whichever payload we obtained)
    payload = plain_payload or dtls_payload
    if payload is None:
        record("telemetry contract", "SKIP", "no /env/temp payload obtained")
    elif cbor2 is None:
        record("telemetry contract", "SKIP", "cbor2 not installed (pip install cbor2)")
    else:
        try:
            obj = cbor2.loads(payload)
        except Exception:
            obj = None
        if not isinstance(obj, dict):
            record("telemetry contract", "FAIL", f"payload is not a CBOR map: {payload.hex()}")
        elif TELEMETRY_KEYS & set(obj):
            record("telemetry contract", "PASS", f"keys: {sorted(obj)}")
        else:
            # piggyback not chosen — telemetry may live on /sys/health (ADR-007)
            resp, _, _ = await coap_request(
                ctx, aiocoap.GET, f"coap://[{args.node_a}]/sys/health", timeout=5)
            if resp and resp.code.is_successful():
                record("telemetry contract", "PASS", "telemetry on /sys/health (ADR-007 option 2)")
            else:
                record("telemetry contract", "WARN",
                       f"no telemetry keys in {sorted(obj)} and /sys/health unreachable")

    # 4 — valve round-trip (SED: expect ~poll-period latency — Lab 4 physics)
    if args.valve:
        valve_uri = f"coap://[{args.valve}]/act/valve"
        ok = True
        lats = []
        for step, (method, pl, want) in enumerate([
                (aiocoap.PUT, VALVE_OPEN, Code.CHANGED),
                (aiocoap.GET, b"", Code.CONTENT),
                (aiocoap.PUT, VALVE_CLOSE, Code.CHANGED)]):
            resp, lat, err = await coap_request(ctx, method, valve_uri, pl, timeout=20)
            lats.append(lat)
            if resp is None or resp.code != want:
                ok = False
                record("valve round-trip", "FAIL",
                       f"step {step + 1}: {err or resp.code}")
                break
            if method is aiocoap.GET and resp.payload != VALVE_OPEN:
                ok = False
                record("valve round-trip", "FAIL",
                       f"GET returned {resp.payload.hex()}, expected {VALVE_OPEN.hex()}")
                break
        if ok:
            record("valve round-trip", "PASS",
                   f"open/read/close OK, avg {statistics.mean(lats):.0f} ms (SED poll latency)")
    else:
        record("valve round-trip", "SKIP", "no valve address given")

    # 5 — invalid inputs (the automated half of the mini pentest)
    resp, _, _ = await coap_request(ctx, aiocoap.GET,
                                    f"coap://[{args.node_a}]/does/not/exist", timeout=5)
    if plain_open:
        record("unknown path -> 4.04", "PASS" if resp and resp.code == Code.NOT_FOUND else "FAIL",
               "" if resp and resp.code == Code.NOT_FOUND else f"got {resp.code if resp else 'timeout'}")
    else:
        record("unknown path -> 4.04", "SKIP", "plaintext locked out — test via coap-client by hand")
    if args.valve:
        resp, _, _ = await coap_request(ctx, aiocoap.PUT,
                                        f"coap://[{args.valve}]/act/valve", b"\x01", timeout=20)
        good = resp is not None and resp.code == Code.BAD_REQUEST
        record("malformed valve payload -> 4.00", "PASS" if good else "FAIL",
               "" if good else f"got {resp.code if resp else 'timeout'}")

    # 6 — stress: 20 sequential GETs against Node A (not the SED — Lab 4 physics)
    if plain_open:
        lats, ok_count = [], 0
        for _ in range(20):
            resp, lat, _ = await coap_request(ctx, aiocoap.GET, env_temp_uri, timeout=10)
            lats.append(lat)
            if resp is not None and resp.code.is_successful():
                ok_count += 1
        ratio = ok_count / 20
        detail = (f"{ok_count}/20 OK ({ratio:.0%}), "
                  f"latency min/avg/max = {min(lats):.0f}/{statistics.mean(lats):.0f}/{max(lats):.0f} ms")
        record("stress (20 requests)", "PASS" if ratio >= 0.8 else "FAIL", detail)
    else:
        record("stress (20 requests)", "SKIP",
               "plaintext locked out — per-request DTLS handshakes would measure the "
               "handshake, not the server; run by hand with coap-client if needed")

    # 7 — burst: 12 parallel GETs, expect the Lab 8 rate limiter to answer 4.29
    if plain_open:
        burst = await asyncio.gather(
            *(coap_request(ctx, aiocoap.GET, env_temp_uri, timeout=10) for _ in range(12)))
        too_many = sum(1 for resp, _, _ in burst
                       if resp is not None and int(resp.code) == CODE_TOO_MANY_REQUESTS)
        ok_count = sum(1 for resp, _, _ in burst
                       if resp is not None and resp.code.is_successful())
        if too_many:
            record("burst rate-limiting", "PASS",
                   f"{ok_count} served, {too_many}x 4.29 — rate limiter live")
        else:
            record("burst rate-limiting", "WARN",
                   f"{ok_count}/12 served, no 4.29 seen — rate limiter missing or window too generous")
    else:
        record("burst rate-limiting", "SKIP",
               "plaintext locked out — DTLS re-handshakes spread the burst below the window "
               "(see SOP-08 troubleshooting)")

    # report — the success ratio + latency stats here are the Lab 8 deliverable
    print("\n=== Summary ===")
    counts = {s: sum(1 for r in results if r["status"] == s)
              for s in ("PASS", "FAIL", "WARN", "SKIP")}
    for r in results:
        print(f"  {r['status']:4}  {r['name']}" + (f" — {r['detail']}" if r["detail"] else ""))
    print(f"\n{counts['PASS']} passed, {counts['FAIL']} failed, "
          f"{counts['WARN']} warnings, {counts['SKIP']} skipped")
    await ctx.shutdown()
    return counts["FAIL"] == 0


if __name__ == "__main__":
    sys.exit(0 if asyncio.run(main()) else 1)
