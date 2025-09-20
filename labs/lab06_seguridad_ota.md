# Lab 6 — Seguridad & OTA (Lab 11)

## Objetivos
- Threat model básico (activos, amenazas, controles iniciales).
- Integrar MCUboot y firma de imágenes.
- Realizar actualización v1 → v2 (cambio visible: versión en log).
- Documentar pipeline de actualización segura.

## Orden Pedagógico
1. Threat model (tabla activos/amenazas).
2. Habilitar MCUboot (sysbuild / config).
3. Generar clave y firmar imagen v1.
4. Crear v2 con cambio de versión.
5. Validar logs arranque y rollback opcional.

## Miércoles (2h)
- (30m) Teoría seguridad IoT + OTA.
- (30m) Config y build bootloader + imagen v1.
- (30m) Firma y flasheo.
- (30m) Imagen v2 y validación.

## Trabajo Autónomo
- Documentar pipeline paso a paso.
- DDR: D-010 (Modelo amenazas), D-011 (Política actualización).

## Viernes (1h)
- (30m) Revisión logs y fallback.
- (20m) Discusión amenazas residuales.
- (10m) Preview observabilidad.

## Entregables Core
- Logs MCUboot con versión v1 y v2.
- Threat model tabla.
- Evidencia firma (hash o comando).

## Métricas
- Tiempo total actualización (s).
- Tamaño imagen vs overhead firma.

## Opcionales
- Simulación firma inválida (rechazo arranque).