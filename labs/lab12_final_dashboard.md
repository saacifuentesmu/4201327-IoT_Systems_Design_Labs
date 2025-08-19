# Lab 12 — Integración final y dashboard

## Objetivos
- Construir un dashboard para mostrar datos de sensores de nodos Thread vía un Border Router.
- Opción A: Python Flask + proxy CoAP simple; Opción B: Node + fetch desde bridge CoAP→HTTP.

## Pasos (Opción A — Flask)
1) En tu venv de Python, instala Flask y aiocoap.
2) Escribe un servidor Flask que consulte periódicamente `/sensor` por CoAP vía la IP del BR y almacene en caché.
3) Sirve una página con el último valor y un botón para conmutar `/light`.

## Entregable
- Video corto de demo: dashboard leyendo y conmutando un nodo sobre Thread.

## Consejos
- Si hay firewall, ejecuta el dashboard en la misma máquina que OTBR.
- Para mayor confiabilidad, usa CoAP confirmable y reintentos simples.
