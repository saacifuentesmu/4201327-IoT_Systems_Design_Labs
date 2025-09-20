#!/usr/bin/env python3
"""Stub de pruebas E2E para evolucionar hasta el Lab 8.
Actualmente:
 - Mide latencia de N lecturas GET /sensor (simulada).
Extensión futura:
 - Añadir PUT /light, secuencias stress, validación OTA.
"""
import argparse
import asyncio
import statistics
import time
from aiocoap import Context, Message, GET

async def measure(host: str, count: int, path: str):
    uri = f'coap://[{host}]{path}'
    ctx = await Context.create_client_context()
    latencies = []
    for i in range(count):
        req = Message(code=GET, uri=uri)
        start = time.perf_counter()
        try:
            resp = await ctx.request(req).response
        except Exception as e:
            print(f'Fallo {i}: {e}')
            continue
        dt = (time.perf_counter() - start) * 1000
        latencies.append(dt)
        payload = resp.payload.decode(errors='ignore') if resp.payload else ''
        print(f'[{i}] {resp.code} {dt:.2f} ms {payload}')
    if latencies:
        print('\nResumen:')
        print(f' n={len(latencies)} media={statistics.mean(latencies):.2f} ms p95={statistics.quantiles(latencies, n=20)[18]:.2f} ms')

async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--host', required=True, help='IPv6 del nodo')
    ap.add_argument('--count', type=int, default=5)
    ap.add_argument('--path', default='/sensor')
    args = ap.parse_args()
    await measure(args.host, args.count, args.path)

if __name__ == '__main__':
    asyncio.run(main())
