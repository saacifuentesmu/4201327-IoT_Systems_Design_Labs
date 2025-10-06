# Fundamentos de IoT - Ejercicios Prácticos

**Enfoque**: Conceptos fundamentales de IoT usando herramientas modernas (ESP-IDF, OpenThread, ESP32‑C6)

**Metodología**: Capas de red (labs 1‑2) → Redes mesh (labs 3‑4) → Aplicaciones avanzadas (labs 5‑6) → Optimización (labs 7‑8)

Cada lab: 2 horas presenciales + ~3 horas de tarea. Los entregables son incrementales.
Hardware: ESP32‑C6 DevKitC. Placa objetivo: `esp32c6`.

## FASE 1: CAPAS FÍSICAS Y DE ENLACE (Labs 1–2)

Lab 1 — IEEE 802.15.4 Fundamentals (PHY/MAC/Sniffing)
- **Herramienta**: Configurador SDK (GUI) para IEEE 802.15.4 + Spectrum Analyzer
- **Práctica**: Análisis de espectro, CCA y canal, filtros, análisis físico
- **Entregable**: Comparativa de CCA/canales + análisis de interferencia

Lab 2 — 6LoWPAN + Routing & Resiliencia
- **Concepto IoT**: 6LoWPAN, routing Thread, resiliencia de red
- **Proyecto**: Implementar routing 6LoWPAN, observar fragmentación, evaluar re-attach y cambio de roles
- **Herramientas**: ESP-IDF + OpenThread
- **Entregable**: Logs de routing, análisis de fragmentación

## FASE 2: REDES MESH Y COMUNICACIÓN (Labs 3-4)

Lab 3 — Thread/CoAP Basic
- **Herramienta**: ESP‑IDF + ejemplo `openthread/ot_cli` (VS Code Extension)
- **Práctica**: Formación de red Thread, CLI básica, servidor CoAP con recursos `/light` y `/sensor`, pruebas CLI-based
- **Entregable**: Capturas de CLI y pruebas CoAP via CLI

Lab 4 — Sensor Integration and Dashboards
- **Concepto IoT**: Integración sensores, dashboards IoT
- **Proyecto**: Sensor físico o mock en red Thread, dashboard web con control y monitoreo
- **Herramientas**: Flask/Django, sensores I2C, CoAP polling
- **Entregable**: Dashboard funcional con datos en tiempo real

## FASE 3: APLICACIONES AVANZADAS Y OPTIMIZACIÓN (Labs 5-8)

Lab 5 — Thread/CoAP Advanced & Border Router
- **Concepto IoT**: Border routers, patrones pub/sub, CoAP observe
- **Proyecto**: Implementar Border Router RCP, CoAP observe para notificaciones en tiempo real, pruebas network-based
- **Herramientas**: OTBR, CoAP client Python
- **Entregable**: Border Router funcional, demo de observe con cliente network

Lab 6 — Security & OTA
- **Concepto IoT**: Seguridad IoT, actualizaciones OTA seguras
- **Proyecto**: Implementar MCUboot, firma de imágenes, actualización v1→v2
- **Herramientas**: MCUboot, imgtool
- **Entregable**: Firmware actualizado de forma segura, logs de verificación

Lab 7 — Observability & Optimization
- **Concepto IoT**: Métricas de rendimiento, caching, rate limiting
- **Proyecto**: Recolectar métricas, implementar caching y rate limiting
- **Herramientas**: ESP-IDF logging, CoAP
- **Entregable**: Métricas recolectadas, demo de optimizaciones

Lab 8 — Consolidation & Hardening
- **Concepto IoT**: Pruebas end-to-end, hardening de seguridad, documentación
- **Proyecto**: Tests automatizados, mini pentest, documentación completa
- **Herramientas**: Scripts Python, Wireshark
- **Entregable**: Suite de tests, reporte de hardening, documentación final

## Notas Metodológicas
- **DDRs**: Documentar decisiones técnicas y trade-offs en cada fase
- **Enfoque Práctico**: 70% hands-on, 30% teoría
- **Herramientas**: OpenThread/ESP32‑C6 como vehículo, no como objetivo
- **Evaluación**: Proyectos incrementales + examen parcial + demo final
- **Industria**: Casos de uso reales, estándares, best practices
