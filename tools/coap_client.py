#!/usr/bin/env python3
"""Cliente simple para interactuar con /light y /sensor.
Requiere 'aiocoap' instalado en el entorno host.
Uso:
  python coap_client.py --host fdde:ad00:beef::1234 get /sensor
  python coap_client.py --host fdde:ad00:beef::1234 put /light 1
"""
import argparse
import asyncio

from aiocoap import Context, Message, GET, PUT

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True, help='Dirección IPv6 del nodo (sin corchetes)')
    parser.add_argument('method', choices=['get', 'put'])
    parser.add_argument('path', help='Recurso, ej /sensor o /light')
    parser.add_argument('value', nargs='?', help='Valor para PUT (0/1)')
    args = parser.parse_args()

    proto = await Context.create_client_context()

    uri = f'coap://[{args.host}]{args.path}'
    if args.method == 'get':
        req = Message(code=GET, uri=uri)
    else:
        payload = (args.value or '').encode()
        req = Message(code=PUT, uri=uri, payload=payload)

    try:
        resp = await proto.request(req).response
    except Exception as e:
        print('Error:', e)
        return

    print('Code:', resp.code)
    if resp.payload:
        print('Payload:', resp.payload.decode(errors='ignore'))

if __name__ == '__main__':
    asyncio.run(main())
