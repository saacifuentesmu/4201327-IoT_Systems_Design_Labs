# Programa de 8 laboratorios: Fundamentos de IoT - Ejemplos Prácticos

**Enfoque**: Conceptos fundamentales de IoT usando herramientas modernas (ESP-IDF, OpenThread, ESP32‑C6)

**Metodología**: Fundamentos (labs 1‑2) → Redes mesh (labs 3‑4) → Aplicaciones (labs 5‑6) → Optimización (labs 7‑8)

Cada lab: 3 h presenciales + ~3 h de tarea. Los entregables son incrementales.
Hardware: ESP32‑C6 DevKitC, sniffer opcional. Placa objetivo: `esp32c6`.

## FASE 1: FUNDAMENTOS IoT CON ESP‑IDF (Labs 1–2)

Lab 1 — Thread CLI + CoAP base  
- **Herramienta**: ESP‑IDF + ejemplo `openthread/ot_cli` (VS Code Extension)  
- **Práctica**: Formación de red Thread, CLI básica, servidor CoAP con recursos `/light` y `/sensor`  
- **Entregable**: Capturas de CLI y pruebas GET/PUT con `coap-client`

Lab 2 — PHY/MAC + Sniffing  
- **Herramienta**: Configurador SDK (GUI) para IEEE 802.15.4 + Wireshark  
- **Práctica**: Captura de tramas 802.15.4/6LoWPAN, CCA y canal, filtros, análisis  
- **Entregable**: PCAP anotado + comparativa de CCA/canales
## FASE 2: REDES MESH Y COMUNICACIÓN (Labs 3-4)

Lab 3 — 6LoWPAN + Routing & Resiliencia
- **Concepto IoT**: 6LoWPAN, routing Thread, resiliencia de red
- **Proyecto**: Implementar routing 6LoWPAN, observar fragmentación, evaluar re-attach y cambio de roles
- **Herramientas**: ESP-IDF + OpenThread
- **Entregable**: Logs de routing, análisis de fragmentación

Lab 4 — Border Router + Patrones de Aplicación
- **Concepto IoT**: Border routers, patrones pub/sub, CoAP observe
- **Proyecto**: Implementar Border Router RCP, CoAP observe para notificaciones en tiempo real
- **Herramientas**: OTBR, CoAP client
- **Entregable**: Border Router funcional, demo de observe

## FASE 3: APLICACIONES Y OPTIMIZACIÓN (Labs 5-8)

Lab 5 — Sensores + Dashboard Inicial
- **Concepto IoT**: Integración sensores, dashboards IoT
- **Proyecto**: Sensor físico o mock, dashboard web con control y monitoreo
- **Herramientas**: Flask/Django, sensores I2C
- **Entregable**: Dashboard funcional con datos en tiempo real

Lab 6 — Seguridad & OTA
- **Concepto IoT**: Seguridad IoT, actualizaciones OTA seguras
- **Proyecto**: Implementar MCUboot, firma de imágenes, actualización v1→v2
- **Herramientas**: MCUboot, imgtool
- **Entregable**: Firmware actualizado de forma segura, logs de verificación

Lab 7 — Observabilidad & Optimización
- **Concepto IoT**: Métricas de rendimiento, caching, rate limiting
- **Proyecto**: Recolectar métricas, implementar caching y rate limiting
- **Herramientas**: ESP-IDF logging, CoAP
- **Entregable**: Métricas recolectadas, demo de optimizaciones

Lab 8 — Consolidación & Hardening
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
