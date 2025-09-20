# Plan de Laboratorios (8 Semanas)

Este documento resume la organización de los 8 laboratorios combinados para el ciclo Semana 5–Semana 12.

| Semana | Lab Combinado | Labs Originales | Foco Principal | Evidencias Clave |
|--------|---------------|-----------------|----------------|------------------|
| 5 | Lab 1 – Thread CLI + CoAP Base | 02 + 03 | Formación de red, roles, endpoints básicos | pcap ping/CoAP, `/light`, `/sensor` mock |
| 6 | Lab 2 – PHY + MAC + Sniffing | 04 + 05 | Canal, tramas, CCA/backoff | pcap anotado, comparación CCA |
| 7 | Lab 3 – 6LoWPAN + Routing/Resiliencia | 06 + 07 | Direcciones, fragmentación, re-attach | Tabla direcciones, tiempos reconvergencia |
| 8 | Lab 4 – Border Router + App Patterns | 09 + 08 (observe) | OTBR, observe, pub/sub básico | BR funcional, observe `/sensor` |
| 9 | Lab 5 – Sensores + Dashboard Inicial | 10 + parte 12 | Sensor físico/mock, energía, dashboard mínimo | JSON `/sensor`, dashboard básico |
| 10 | Lab 6 – Seguridad & OTA | 11 | MCUboot, firma, threat model | Logs MCUboot, upgrade v1→v2 |
|11 | Lab 7 – Observabilidad & Optimización | 12 (resto) | Métricas, caching, streaming opcional | Latencia, token simple, SSE/WebSocket opcional |
|12 | Lab 8 – Consolidación & Hardening | (Integración final) | Testing, performance, mini pentest, documentación | Script test E2E, video demo |

## Filosofía
- Cada lab produce artefactos reutilizables (scripts, pcap, configs, claves).
- El documento DDR se actualiza incrementalmente (un solo archivo).
- Opcionales permiten diferenciación sin bloquear progreso core.

## Roles y Grupos
- Grupos de 3 estudiantes. Hasta 6 placas por grupo permiten paralelismo (2 para red base, 1 RCP/BR, 1 sensor, 1 pruebas resiliencia, 1 fallback).

## Rúbrica Base
Funcionalidad 40%, Evidencia 25%, Análisis 20%, DDR 10%, Calidad 5%.

