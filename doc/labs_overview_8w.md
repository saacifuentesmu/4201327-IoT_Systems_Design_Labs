# Plan de Laboratorios (8 Semanas)

Este documento resume la organización de los 8 laboratorios combinados para el ciclo Semana 5–Semana 12.

| Semana | Lab | Foco Principal | Evidencias Clave |
|--------|----|----------------|------------------|
| 5 | Lab 1 – IEEE 802.15.4 Fundamentals | Canal, tramas, CCA/backoff | comparación CCA, análisis espectro |
| 6 | Lab 2 – 6LoWPAN + Routing/Resiliencia | Direcciones, fragmentación, re-attach | Tabla direcciones, tiempos reconvergencia |
| 7 | Lab 3 – Thread/CoAP Basic | Formación de red, roles, endpoints básicos (CLI-based) | pcap ping/CoAP, `/light`, `/sensor` mock |
| 8 | Lab 4 – Sensor Integration and Dashboards | Sensor físico/mock, energía, dashboard mínimo | JSON `/sensor`, dashboard básico |
| 9 | Lab 5 – Thread/CoAP Advanced & Border Router | OTBR, observe, pub/sub básico | BR funcional, observe `/sensor` |
| 10 | Lab 6 – Security & OTA | MCUboot, firma, threat model | Logs MCUboot, upgrade v1→v2 |
|11 | Lab 7 – Observability & Optimization | Métricas, caching, streaming opcional | Latencia, token simple, SSE/WebSocket opcional |
|12 | Lab 8 – Consolidation & Hardening | Testing, performance, mini pentest, documentación | Script test E2E, video demo |

## Filosofía
- Cada lab produce artefactos reutilizables (scripts, pcap, configs, claves).
- El documento DDR se actualiza incrementalmente (un solo archivo).
- Opcionales permiten diferenciación sin bloquear progreso core.

## Roles y Grupos
- Grupos de 3 estudiantes. Hasta 6 placas por grupo permiten paralelismo (2 para red base, 1 RCP/BR, 1 sensor, 1 pruebas resiliencia, 1 fallback).

## Rúbrica Base
Funcionalidad 40%, Evidencia 25%, Análisis 20%, DDR 10%, Calidad 5%.

