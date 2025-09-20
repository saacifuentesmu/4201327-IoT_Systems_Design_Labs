# Lab 2 — PHY + MAC + Sniffing (Fusión Labs 04 + 05)

## Objetivos
- Comprender canalización 2.4 GHz y tramas 802.15.4.
- Capturar y clasificar Beacon, Data, Ack, MAC Command.
- Evaluar impacto de CCA threshold y backoff.

## Orden Pedagógico
1. Revisión rápida pcap Lab 1.
2. Espectro y canales (canal elegido vs interferencia).
3. Sniffing y clasificación de tramas.
4. Escaneos energy/active y tabla comparativa.
5. Ajuste `CONFIG_IEEE802154_ESP32_CCA_THRESHOLD` y nueva captura.

## Miércoles (2h)
- (25m) Teoría PHY/MAC.
- (35m) Captura base (red ya formada).
- (30m) Escaneos (`ot scan energy`, `ot scan active`).
- (20m) Cambiar threshold y rebuild.
- (10m) Captura comparativa.

## Trabajo Autónomo
- Anotar RSSI medio y variabilidad (5 distancias).
- Tabla antes/después CCA (nº retransmisiones / tramas fallidas si observable).
- DDR: D-003 (Threshold CCA decisión).

## Viernes (1h)
- (20m) Revisión capturas.
- (30m) Discusión interferencia y mitigación.
- (10m) Avance lectura 6LoWPAN fragmentación.

## Entregables Core
- pcap anotado (mín 30 s) + lista de tramas.
- Tabla escaneos energy/active.
- Comparación threshold (texto breve).

## Métricas
- RSSI medio por distancia.
- Diferencia frames perdidos (si medible) antes/después.

## Opcionales
- Gráfico RSSI vs distancia.
- Script parse pcap (tshark) para contar tipos de tramas.