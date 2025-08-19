# Lab 06 — 6LoWPAN e IPv6

## Objetivos
- Enumerar direcciones IPv6 en nodos Thread.
- Forzar fragmentación 6LoWPAN con payloads grandes.

## Pasos
1) En cada nodo: `ot ipaddr` y `net iface` — registrar ML‑EID, mesh‑local, link‑local.
2) Usar CoAP para enviar payloads > 80 bytes que disparen la fragmentación.
3) Capturar para verificar headers y fragmentos 6LoWPAN.

## Verificación
- Tabla de direcciones y evidencia de intercambio fragmentado.
