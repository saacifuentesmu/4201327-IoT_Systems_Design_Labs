# Lab 3 — 6LoWPAN + Routing & Resiliencia (Fusión Labs 06 + 07)

## Objetivos
- Enumerar y clasificar direcciones IPv6 (link-local, mesh-local, ML-EID).
- Observar fragmentación 6LoWPAN.
- Evaluar re-attach y cambio de roles (líder, routers, children).

## Orden Pedagógico
1. Direcciones y prefijos.
2. Fragmentación forzada (payload > 80B CoAP PUT/POST ficticio).
3. MLE messages y re-attach inducido (mover nodo / apagar líder).
4. Medición tiempos convergencia.

## Miércoles (2h)
- (20m) Teoría 6LoWPAN compresión y fragmentación.
- (40m) Tabla direcciones nodos.
- (30m) Fragmentación (captura pcap confirmando headers).
- (20m) Escenario re-attach (apagar líder).
- (10m) Registro tiempos.

## Trabajo Autónomo
- Repetir test re-attach 3 veces y promediar.
- DDR: D-004 (Sizing MTU / fragmentación) D-005 (Resiliencia approach).

## Viernes (1h)
- (25m) Revisión fragmentos pcap.
- (25m) Discusión tuning topología.
- (10m) Preview Border Router.

## Entregables Core
- Tabla direcciones.
- pcap fragmentación con mínimo 2 fragmentos.
- Tiempos re-attach (ms) + líder nuevo identificado.

## Métricas
- Latencia re-attach promedio.
- Nº fragmentos vs payload size.

## Opcionales
- Gráfico tiempo re-attach vs pérdida simulada.