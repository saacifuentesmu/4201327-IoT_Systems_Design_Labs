# SOP-05: OpenThread Border Router (OTBR) Deployment

> **Lab guide:** [Lab 5](../lab5.md) — read it first; the networking-pattern artifact, tasks, and DDR deliverables live there.
> **This SOP:** RCP flash, OTBR firmware build, commissioning, end-to-end reach test, troubleshooting. Total student-authored C: **zero**. Both firmwares come straight from `$IDF_PATH/examples/openthread/`.

The Thread mesh from [Lab 2](../lab2.md), the `/env/temp` server from [Lab 3](../lab3.md), and the `/act/valve` server from [Lab 4](../lab4.md) are prerequisites. ESP-IDF v5.1+. **Additional hardware required for this lab:**

- 1× **ESP32-S3-DevKitC-1** (Border Router *host*; needs Wi-Fi, the C6 already in the mesh does not have it)
- 1× **ESP32-C6-DevKitC-1** dedicated as **RCP** (Radio Co-Processor — a 5th board, *in addition to* Nodes A / B / V from Labs 3–4)
- 4× male-to-female jumper wires (RCP UART → S3 UART) or a USB-to-UART bridge
- Wi-Fi network the S3 can join (your laptop's hotspot is fine for the lab)

**Why two boards.** The S3 has Wi-Fi but no 802.15.4 radio; the C6 has 802.15.4 but a less-capable Wi-Fi (and the OTBR Linux stack expects an *external* radio). The C6 runs as an **RCP** — a "dumb modem" exposing its radio over UART using the Spinel protocol. The S3 runs the OTBR application and drives the RCP. Together they form one logical Border Router.

---

## 1. Flash the Radio Co-Processor (RCP)

The RCP firmware ships in ESP-IDF. No student C.

```bash
cd $IDF_PATH/examples/openthread/ot_rcp
idf.py set-target esp32c6
idf.py build
idf.py -p /dev/ttyUSB_RCP flash       # the C6 you're dedicating as RCP
```

Pick a USB port name that you can keep straight from your other C6 boards — `/dev/ttyUSB_RCP` is a symlink suggestion; use the actual device path on your machine. **Note the port:** the OTBR host needs it.

Once flashed, this board does *nothing visible*. It has no CLI, no LEDs of consequence. It only speaks Spinel-over-UART when the host asks it to. If you `idf.py monitor` you'll see startup logs and then silence — that's correct.

> **Wiring it to the S3 host.** The simplest option is **USB-to-USB**: plug the C6-RCP into one USB port on the laptop, the S3 into another, and tell the OTBR host the C6's serial device. No jumper wires. Espressif's `ot_br` example expects exactly this by default and the SOP assumes it. (Direct UART-to-UART between the two boards is also supported — see [Espressif's OTBR docs](https://github.com/espressif/esp-idf/tree/master/examples/openthread/ot_br) — but it adds Kconfig steps that don't pay off for the lab.)

---

## 2. Flash and launch the OTBR host

```bash
cd $IDF_PATH/examples/openthread/ot_br
idf.py set-target esp32s3
idf.py menuconfig
```

In `menuconfig`, three settings to set (everything else can stay default):

```
Example Connection Configuration → WiFi SSID         = <your network SSID>
Example Connection Configuration → WiFi Password     = <password>
Component config → OpenThread → Spinel UART
        Spinel UART device          = /dev/ttyUSB_RCP   # the RCP's serial port
        Spinel UART baudrate        = 460800             # ot_rcp default
```

Save, exit, build, flash:

```bash
idf.py build
idf.py -p /dev/ttyUSB_S3 flash monitor
```

On the S3 monitor you'll see the Wi-Fi association first, then the OTBR coming up. The line that confirms the radio is alive is:

```
I (4321) OPENTHREAD: Platform UART init done
I (4400) OPENTHREAD: NCP started
I (4521) OT_BR: BR is started
```

The S3 prints its **Wi-Fi IPv4** in this same log block (`got ip:192.168.x.x`). That's the address you open in the browser.

---

## 3. Form the network from the OTBR web UI

Open `http://<S3 Wi-Fi IPv4>/` in a browser. The OTBR web UI loads. (No HTTPS; that's Lab 6.)

1. **Set a password.** First thing the UI prompts for; do not skip. The OTBR is now reachable from anyone on the same Wi-Fi.
2. **Form** a new network. Pick:
   - **Network name:** anything memorable, e.g. `SoilSense-OTBR`
   - **PAN ID:** non-default, four hex digits (e.g. `0xCAFE`) — same constraint as [SOP-02](sop02_6lowpan.md)
   - **Channel:** 15 (or whatever your room uses — avoid Wi-Fi channel 6's neighborhood, 2.405–2.485 GHz overlap)
   - **Network key:** auto-generate, copy it
3. Click **Form**. The UI says "Network formed" and switches to the **Topology** view with one node (the OTBR itself).
4. **Verify a global prefix is being advertised.** Go to **Network → Settings**. The default Espressif build enables the `Prefix` advertisement with `paros` flags (preferred, valid SLAAC, on-mesh, default-route, stable). If `paros` flags are not set, add the prefix manually — `fd<six random hex>::/64`, `paros` flags ticked.

The OTBR's web UI is also where commissioning settings live, but for the lab we use the dataset-paste method below (faster, no joiner steerable session).

---

## 4. Re-commission Node A and Node V onto the OTBR-formed mesh

The Lab 3 and Lab 4 boards are still running their existing CoAP server firmware (`/env/temp` on Node A; `/act/valve` on Node V). You don't reflash them — you only move them to the new network.

On the OTBR web UI's Topology page, click **Dataset**. Copy the long hex string under "Active Dataset".

On each of Node A and Node V:

```
> dataset clear
> dataset set active <paste hex>
> ifconfig up
> thread start
```

After 30–60 s, `state` on each should report `child` or `router` (Node V is MTD/SED → `child`, Node A is FTD → `router`). The OTBR topology page refreshes and shows them as neighbors.

Node B (the CLI client from Labs 3–4) — your call. If you want to keep an in-mesh client around for the Task C baseline measurement, re-commission it the same way. Otherwise leave it on the old network and skip the in-mesh baseline.

---

## 5. Confirm global addresses on the nodes

On Node A (after it joined):

```
> ipaddr
fd<otbr-mesh-local>::1                  ← mesh-local EID, only valid inside the mesh
fd<otbr-global-prefix>::ff:fe00:0001    ← global, derived from the prefix the OTBR advertised
fe80::1234:5678:9abc:def0               ← link-local, normal
```

You should see **at least two non-link-local** addresses now (mesh-local + global), where Lab 3/4 you only saw one. The second one — the global — is what an external client (your laptop, on Wi-Fi) targets.

`ipaddr mleid` still returns the mesh-local one (unchanged from Lab 3/4).

Do the same on Node V. Both nodes should report a global address with the **same prefix** the OTBR advertised in §3.

---

## 6. Task C — measure the OTBR's added latency

### 6.1 In-mesh baseline (reproduce the Lab 3 number)

From Node B's CLI (assuming you kept it on the OTBR-formed mesh):

```
> coap start
> coap get fd<...>::A /env/temp        ← Node A's mesh-local address
```

Time 10 round-trips. Median should match your Lab 3 baseline within ±20 ms.

### 6.2 Through the OTBR — from your laptop on Wi-Fi

The laptop already has the OTBR's global prefix routed to it because the OTBR sent a Router Advertisement on its Wi-Fi side. Confirm:

```bash
ping6 -c 3 fd<otbr-global-prefix>::ff:fe00:0001     # Node A's global IPv6
```

You should get replies. If not, see Troubleshooting.

Now hit the CoAP server from the laptop using the project's existing Python client:

```bash
python tools/coap_client.py --host "fd<otbr-global-prefix>::ff:fe00:0001" get /env/temp
```

The 6-byte CBOR comes back, identical to what Node B saw in §6.1 — same `a16174f9....` bytes. Time 10 round-trips. The delta vs §6.1 is the OTBR's added cost.

### 6.3 NAT64 — Thread sensor pings the IPv4 internet

NAT64 is enabled by default in Espressif's ot_br with the `64:ff9b::/96` prefix. From Node A's CLI:

```
> ping 64:ff9b::8.8.8.8
```

You should see replies. Failures here usually mean the OTBR's upstream DNS64 isn't resolving (Espressif's ot_br implements NAT64 *translation*, but if you used a literal IPv4-mapped IPv6 form the request still needs to leave the AP — your home router has to actually route IPv6 out, which not every consumer router does). If your AP is IPv6-only at the WAN, this works; if it's IPv4-only at the WAN, you may see "no route". That's an interesting fact for your DDR §5, not a failure of the lab — record what happened.

---

## 7. (Optional) End-to-end from outside the LAN

**Not required for the lab.** If you want to demonstrate the full four-network walk (Daniela on her phone, off your Wi-Fi) you have two options:

- **Tailscale / ZeroTier / Tunnel:** put the laptop CoAP client on a tunnel; the phone joins the tunnel; the CoAP path is laptop-routed. Simple, doesn't expose anything publicly.
- **Public CoAP test server as the "cloud":** modify Node A to *also* be a CoAP client that POSTs to `coap.me` periodically. Wireshark on the OTBR side will show the packets leaving via NAT64.

Either way, the bytes on the wire are still the same `/env/temp` CBOR. The boundary between "services" and "user" networks (Table A.4) is below the application — the OTBR doesn't care.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| OTBR web UI shows no global prefix in Routes | The `paros` flags weren't set on the prefix. In **Network → Settings**, add `fd<six hex>::/64` with `paros` ticked. Or set `OPENTHREAD_BR_AUTO_START_OMR` = `y` in menuconfig before re-flashing. |
| `ipaddr` on Node A shows only mesh-local + link-local (no global) | The node joined the mesh *before* the prefix was advertised. `ifconfig down; ifconfig up; thread start` on the node to re-SLAAC. |
| Laptop `ping6` to the global address times out | (1) The OTBR is not advertising a default route — check **Network → Settings → Default Route**, must be ticked. (2) Your laptop's Wi-Fi has IPv6 disabled; turn it on in network settings. (3) Your AP filters IPv6 RAs — try a phone hotspot instead. |
| `coap get` from the laptop returns "no route to host" but `ping6` works | The CoAP client is binding the wrong source interface. Pass `--bind-iface` (or set `IPV6_BOUND_IF` env var) to force the Wi-Fi interface. |
| `ping 64:ff9b::8.8.8.8` from Node A → "Error 13: No route to host" | NAT64 prefix not installed. Check that `CONFIG_OPENTHREAD_BR_AUTO_START_NAT64` is `y` in menuconfig. |
| RCP not detected by S3 (`NCP not responding`) | Check `Spinel UART device` path in menuconfig matches the actual `/dev/ttyUSB*` for the RCP. On Linux, `dmesg \| tail` after plugging in the RCP tells you the path. |
| Node A's old `dataset` from Lab 3 prevents joining | `dataset clear` *before* `dataset set active`. The CLI doesn't overwrite the existing dataset automatically. |
| `state` stays `detached` on Node A after re-commissioning | Channel mismatch — the OTBR auto-picks a channel that may differ from your Lab 3 dataset. The `dataset set active <hex>` *includes* the channel; if you typed it instead of pasted, retype carefully or paste again. |
| OTBR web UI is unreachable from the laptop | The S3 didn't get Wi-Fi. Check the S3 monitor for `wifi:connected, ip:...`. If it failed, the SSID/password in menuconfig are wrong, or the AP is 5 GHz only (the S3 is 2.4 GHz). |

---

## Verification checklist (what to put in your DDR)

- [ ] OTBR web UI **topology screenshot** showing OTBR + Node A + Node V as neighbors.
- [ ] Node A `ipaddr` output, annotated: which line is mesh-local, which is global. Same for Node V.
- [ ] Task C three-row latency table from [lab5.md §4](../lab5.md#task-c--end-to-end-reach-and-the-latency-it-costs-the-headline-number) with all rows filled.
- [ ] Evidence that the local mesh survived an OTBR kill — from Node B (in-mesh), a `coap put` to Node V's *mesh-local* address still landed after the OTBR was stopped. (`thread stop` on the OTBR's S3.)

---

## Appendix — Optional: putting the dashboard back in (stretch goal)

**Not required for the lab.** The Lab 3 dashboard appendix decoded notifications from Node B's monitor stream. Now that the OTBR exposes a routable address for `/env/temp`, you can run the dashboard **on your laptop** instead of pulling notifications from a serial pipe — it makes CoAP look ordinary (over Wi-Fi).

```bash
pip install aiocoap flask
python tools/dashboard_coap.py --remote "fd<global-prefix>::ff:fe00:0001" --resource /env/temp --observe
```

Open `http://localhost:5000`. Same Chart.js view as Labs 0 / 0.5 / 3. What changed: the dashboard now subscribes via CoAP Observe *over Wi-Fi → OTBR → Thread* — three networks of Table A.4 in one path. This is the configuration we make first-class in Lab 6 once DTLS is added.

> **Why we keep this optional in Lab 5:** the lab's headline is the **boundary** and its **latency cost**, not the visualization. The web UI's topology view and the Task C table answer the rubric. Dashboard is for the demo, not the grade.
