# Lab 5 — Sensores + Dashboard Inicial (Fusión Lab 10 + parte Lab 12)

## Objetivos
- Integrar sensor físico (I2C) o mock estructurado.
- Exponer lectura vía CoAP JSON.
- Gestionar energía (sleep entre muestras) y medir duty cycle.
- Construir dashboard mínimo (Flask o stack elegido) lectura + control `/light`.

## Orden Pedagógico
1. Driver / mock sensor.
2. Endpoint `/sensor` JSON estable.
3. PM básico (sleep) y logs timestamps.
4. Servicio recolector (polling o observe ya existente) → almacenar histórico.
5. Dashboard: tabla + último valor + toggle.

## Miércoles (2h)
- (20m) Teoría energía y duty cycle.
- (50m) Sensor + endpoint.
- (30m) PM básico y logging.
- (20m) Recolector + estructura dashboard.

## Trabajo Autónomo
- Completar frontend simple.
- Calcular duty cycle (tiempo activo / intervalo total).
- DDR: D-008 (Estrategia PM), D-009 (Formato datos dashboard).

## Viernes (1h)
- (30m) Demo rápidos dashboards.
- (20m) Revisión duty cycle.
- (10m) Preview seguridad.

## Entregables Core
- Captura dashboard funcionando.
- Log mostrando sleep/awake.
- Duty cycle estimado (%).

## Métricas
- Latencia lectura promedio.
- Duty cycle.

## Opcionales
- InfluxDB + gráfico histórico.