# Lab 10 — Sensores y gestión de energía — Curso IoT ESP32‑C6

## Objetivos
- Leer un sensor I2C simple en Zephyr y exponerlo vía CoAP.
- Aplicar gestión básica de energía (dormir entre muestras).

## Hardware
- Cualquier sensor I2C soportado (p. ej., BME280) o usar un valor simulado si no está disponible.

## Pasos
1) Habilitar I2C y el driver del sensor en `prj.conf` (o mock un valor con un contador).
2) Leer sensor en un intervalo usando una work queue o k_timer.
3) Exponer endpoint `/sensor` vía CoAP retornando JSON (p. ej., `{ "t": 23.5 }`).
4) Agregar PM básico:
   - `CONFIG_PM=y`
   - Dormir entre lecturas con `k_sleep(K_SECONDS(X))`.
5) Medir impacto (si hay medidor de corriente disponible); si no, registrar timestamps.

## Verificación
- CoAP GET `/sensor` retorna datos estructurados.
- Evidencia de ciclo de trabajo (logs o medición).
