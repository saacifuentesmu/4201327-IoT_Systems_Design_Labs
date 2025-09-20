# Lab 1 — Thread CLI + CoAP Base (Fusión Labs 02 + 03)

## Objetivos
- Formar una red Thread mínima (roles, dataset, direccionamiento básico).
- Implementar endpoints `/light` (GET/PUT) y `/sensor` (GET mock JSON) sobre CoAP.
- Comprender CoAP vs HTTP (overhead, métodos, códigos respuesta).

## Orden Pedagógico
1. Thread roles & dataset.
2. Direcciones IPv6 rápidas (solo listar `ipaddr`).
3. Introducción CoAP (modelo REST reducido).
4. Implementación recursos (servidor) en `lab_base`.
5. Cliente CoAP usando CLI en segundo nodo.

## Miércoles (2h)
- (20m) Teoría: Thread basics, CoAP overview.
- (40m) Formar red + script dataset + ping.
- (30m) Añadir handler `/light` y `/sensor` (valor simulado contador o random).
- (10m) Prueba GET/PUT y pequeña captura pcap (5–10 s).

## Trabajo Autónomo
- Medir RTT CoAP vs ping (5 muestras) y documentar.
- Escribir breve comparación CoAP vs HTTP (tabla). 
- Preparar DDR entradas D-001 (CoAP elección) y D-002 (dataset params).

## Viernes (1h)
- (35m) Troubleshooting + validación endpoints.
- (10m) Avance lectura PHY (prep Lab 2).

## Entregables Core
- pcap corto (ping + 2 operaciones CoAP).
- Capturas shell `state`, `ipaddr`.
- Log de toggling `/light`.

## Métricas
- Latencia media CoAP GET (ms).
- Diferencia promedio ping vs CoAP GET.

## Extensiones Futuras
El código de recursos se ampliará en Lab 4 (observe) y Lab 5 (sensor físico).
