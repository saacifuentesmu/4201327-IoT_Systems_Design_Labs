# Lab 7 — Observabilidad & Optimización (Resto Lab 12 + Métricas)

## Objetivos
- Recolectar métricas (latencia, pérdida, throughput notificaciones).
- Implementar caching y rate limiting en dashboard.
- (Opcional) Streaming (WebSocket/SSE) para actualizaciones push.
- Añadir token simple de acceso (hardcoded o .env).

## Orden Pedagógico
1. Métricas definiciones y colección.
2. Capa caching (memoria) + invalidación.
3. Rate limiting (ej: 1 req/s por IP).
4. Streaming opcional.
5. Token auth.

## Miércoles (2h)
- (25m) Teoría observabilidad.
- (45m) Instrumentación métricas código.
- (30m) Caching + rate limiting.
- (20m) Token auth.

## Trabajo Autónomo
- Añadir streaming si hay tiempo.
- DDR: D-012 (Estrategia métricas), D-013 (Caching policy).

## Viernes (1h)
- (30m) Revisión métricas recolectadas.
- (20m) Discusión trade-offs caching.
- (10m) Preparar consolidación final.

## Entregables Core
- Tabla métricas (latencia media, p95, pérdida). 
- Evidencia caching (tiempos antes/después).
- Token activo (demostración simple).

## Opcionales
- SSE/WebSocket.
- Export Prometheus.