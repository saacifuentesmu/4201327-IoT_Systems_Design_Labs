# Programa de 8 laboratorios: Fundamentos de IoT - Ejemplos Prácticos

**Enfoque**: Conceptos fundamentales de IoT usando herramientas modernas (ESP-IDF, OpenThread, ESP32‑C6)
**Metodología**: Fundamentos (labs 1‑2) → Redes mesh (labs 3‑4) → Aplicaciones (labs 5‑6) → Optimización (labs 7‑8)

Cada lab: 3 h presenciales + ~3 h de tarea. Los entregables son incrementales.
Hardware: ESP32‑C6 DevKitC, sniffer opcional. Placa objetivo: `esp32c6`.

## FASE 1: FUNDAMENTOS IoT CON EJEMPLOS ZEPHYR (Semanas 1-3)

Semana 1 — Ecosistema Embebido y RTOS para IoT
- **Concepto IoT**: ¿Qué hace único a los sistemas IoT? Constraints, escala, conectividad.
- **Herramienta**: Entorno Zephyr + ejemplo `samples/hello_world` y `samples/basic/blinky`
- **Práctica**: Setup completo, build/flash, monitoreo serial
- **Tarea**: Explorar `samples/sensor/sensor_shell` - entender drivers y abstracción de hardware
- **Entregable**: Reporte de setup + comparación RTOS vs OS tradicional para IoT

Semana 2 — Conectividad inalámbrica y formación de redes
- **Concepto IoT**: Topologías de red IoT, mesh vs star, auto-configuración
- **Herramienta**: `samples/net/openthread/shell` como ejemplo de red mesh auto‑configurable
- **Práctica**: Formar red Thread entre 3-4 nodos, observar elección de leader, join process
- **Tarea**: Análisis comparativo Thread vs WiFi vs Zigbee para casos de uso IoT
- **Entregable**: Red funcional + DDR-001 (Decision Document Record) sobre topologías

Semana 3 — Protocolos de aplicación para dispositivos constreñidos
- **Concepto IoT**: REST para IoT, CoAP vs HTTP, eficiencia en redes constreñidas
- **Herramienta**: `samples/net/openthread/coap` (cliente/servidor)
- **Práctica**: Implementar recursos `/sensor`, `/actuator` usando el ejemplo base
- **Tarea**: Comparar overhead CoAP vs HTTP, medir tiempos de respuesta
- **Entregable**: Sistema cliente-servidor + análisis de performance

## FASE 2: DESARROLLO PROPIO - CONCEPTOS IoT PROFUNDOS (Semanas 4-8)

Semana 4 — Capa física y análisis de tráfico IoT
- **Concepto IoT**: Espectro electromagnético, interferencia, coexistencia de protocolos (WiFi/BLE/802.15.4)
- **Proyecto**: Desarrollar analizador de espectro simple, medir RSSI, caracterizar entorno RF
- **Herramientas**: Sniffer 802.15.4, Wireshark, mediciones de campo
- **Entregable**: Mapa RF del laboratorio + recomendaciones de despliegue

Semana 5 — Capa MAC y eficiencia energética
- **Concepto IoT**: Duty cycling, sleep modes, energy harvesting, lifetime estimation
- **Proyecto**: Implementar nodo sensor con gestión inteligente de energía
- **Base**: Expandir ejemplos `samples/sensor/` con power management
- **Entregable**: Nodo sensor con >1 año de vida estimada en batería

Semana 6 — Internetworking y direccionamiento
- **Concepto IoT**: IPv6 para IoT, 6LoWPAN, address assignment, mobility
- **Proyecto**: Gateway multi-protocolo (Thread ↔ WiFi ↔ Ethernet)  
- **Base**: `samples/net/openthread/border_router` como punto de partida
- **Entregable**: Gateway funcional + análisis de latencia end-to-end

Semana 7 — Tolerancia a fallos y escalabilidad
- **Concepto IoT**: Network partitions, self-healing, leader election, scalability limits
- **Proyecto**: Red mesh resiliente, simulación de fallas, métricas de recuperación
- **Enfoque**: Arquitecturas distribuidas, consensus algorithms aplicados a IoT
- **Entregable**: Red de 10+ nodos con tolerancia a fallas demostrada

Semana 8 — Observabilidad y métricas
- **Concepto IoT**: Monitoring distribuido, telemetría, anomaly detection
- **Proyecto**: Sistema de telemetría completo (recolección → procesamiento → visualización)
- **Stack**: MQTT/InfluxDB/Grafana como infraestructura de monitoring
- **Entregable**: Dashboard de métricas IoT + alertas automáticas + **Examen Parcial**

## FASE 3: INTEGRACIÓN Y APLICACIONES REALES (Semanas 9-12)

Semana 9 — Patrones de comunicación avanzados
- **Concepto IoT**: Pub/Sub vs Request/Response, event-driven architectures, QoS
- **Proyecto**: Implementar MQTT-SN o CoAP observe para notificaciones asíncronas
- **Aplicación**: Smart building con sensores distribuidos y actuadores
- **Entregable**: Sistema reactivo con eventos en tiempo real

Semana 10 — Edge computing e integración de sensores
- **Concepto IoT**: Edge vs Cloud processing, latency requirements, data fusion
- **Proyecto**: Nodo edge que procesa múltiples sensores, machine learning básico
- **Aplicación**: Predictive maintenance o environmental monitoring  
- **Entregable**: Sistema edge con processing local + optimizaciones de ancho de banda

Semana 11 — Seguridad IoT y actualizaciones OTA
- **Concepto IoT**: Threat models para IoT, secure boot, credential management, firmware updates
- **Proyecto**: Implementar pipeline seguro de OTA usando MCUboot + firma digital
- **Enfoque**: Device identity, commissioning seguro, defense in depth
- **Entregable**: Sistema con OTA seguro + análisis de security posture

Semana 12 — Sistemas completos e integración cloud
- **Concepto IoT**: Cloud connectivity, digital twins, API design, deployment patterns
- **Proyecto Final**: Sistema IoT completo (sensors → edge → cloud → dashboard → mobile)
- **Tecnologías**: REST APIs, cloud functions, database integration
- **Entregable**: Demo final + documentación completa + deployment guide

## Notas Metodológicas
- **DDRs**: Documentar decisiones técnicas y trade-offs en cada fase
- **Enfoque Práctico**: 70% hands-on, 30% teoría  
- **Herramientas**: OpenThread/ESP32‑C6 como vehículo, no como objetivo
- **Evaluación**: Proyectos incrementales + examen parcial + demo final
- **Industria**: Casos de uso reales, estándares, best practices
