# Lab 4 — Border Router + Patrones de Aplicación (Fusión Labs 09 + 08 parcial)

## Objetivos
- Implementar un Border Router (OTBR) con RCP ESP32-C6.
- Acceder nodos Thread desde LAN (ping, CoAP).
- Añadir CoAP Observe al recurso `/sensor`.
- (Opcional) Introducir MQTT (broker local) como comparación pub/sub.

## Orden Pedagógico
1. RCP build + OTBR docker / nativo.
2. Ver conectividad LAN→Thread.
3. CoAP Observe flujo (registro + notificaciones).
4. Métricas entrega (ratio y latencia notificación).
5. (Opcional) MQTT bridging.

## Miércoles (2h)
- (25m) Arquitectura gateway.
- (45m) RCP + OTBR operativo.
- (30m) Implementar observe `/sensor` (timer incrementa valor).
- (20m) Medir latencia notificación.

## Trabajo Autónomo
- Script Python suscriptor observe (aiocoap) registrando timestamps.
- DDR: D-006 (Elección Observe vs polling), D-007 (Gateway deployment).

## Viernes (1h)
- (30m) Validación notificaciones.
- (20m) Discusión MQTT vs CoAP observe.
- (10m) Preparar sensor físico.

## Entregables Core
- Gateway funcional (log OTBR + ping desde host).
- Serie de 5+ notificaciones observe con timestamps.

## Métricas
- Latencia notificación promedio.
- Tasa entrega (recibidas / enviadas).

## Opcionales
- MQTT publish cada X segundos y comparación jitter.