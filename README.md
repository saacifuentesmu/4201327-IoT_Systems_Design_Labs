# Curso de IoT - Fundamentos Prácticos

## Resumen del Curso

Este es un curso práctico de 8 laboratorios centrado en los **fundamentos de IoT** usando ejemplos reales con ESP-IDF. Utiliza ESP32-C6 DevKitC y OpenThread como herramientas prácticas para explorar conceptos clave de IoT: conectividad mesh, protocolos de aplicación, gestión de energía, y sistemas distribuidos.

### Metodología de Aprendizaje
El curso progresa a través de fases estructuradas:
- **Labs 1-2**: Capas físicas y de enlace (IEEE 802.15.4, 6LoWPAN)
- **Labs 3-4**: Redes mesh y comunicación básica (Thread/CoAP, sensores)
- **Labs 5-6**: Aplicaciones avanzadas (Border Router, seguridad/OTA)
- **Labs 7-8**: Observabilidad y consolidación

## Documentación del Curso

- 📋 **[Programa Detallado](doc/syllabus.md)** - Cronograma semanal y objetivos de aprendizaje
- 📅 **[Plan de Laboratorios](doc/labs_overview_8w.md)** - Organización semanal de los 8 labs
- ⚙️ **[Configuración del Entorno](doc/setup.md)** - Guía completa de instalación (Windows nativo, Python, VS Code Extension + ESP‑IDF)
- 🧪 **[Laboratorios](labs/)** - **8 laboratorios** prácticos paso a paso
- 🛠️ **[Herramientas](tools/)** - Scripts auxiliares (CoAP client, test stubs)
- 📝 **[Plantillas](templates/)** - Templates para DDRs y entregables

## Objetivos de Aprendizaje IoT
- Arquitecturas de sistemas IoT distribuidos
- Protocolos de comunicación para dispositivos constreñidos
- Gestión de energía en dispositivos embebidos
- Interoperabilidad y escalabilidad en redes mesh
- Seguridad en sistemas IoT
- Integración con infrastructure cloud/edge

## Herramientas y Tecnologías
**Tecnologías base:** ESP32-C6, ESP-IDF, OpenThread

**Por qué estas herramientas:**
- **ESP32-C6**: SoC moderno con múltiples radios (WiFi, BLE, 802.15.4)
- **ESP-IDF**: Framework oficial de Espressif, con soporte completo para Thread
- **OpenThread**: Implementación open-source de Thread (usado en Matter/Google)

Estas herramientas permiten explorar conceptos IoT sin la complejidad de implementar protocolos desde cero.

## Prerrequisitos de software

1) Instalar Python y Git.
2) Instalar VS Code y la extensión ESP-IDF.
3) Usar la extensión para instalar ESP-IDF v5.1.

## Placas y ejemplos
Placa objetivo: `esp32c6`. Ver documentación de ESP-IDF para ESP32-C6.

Ejemplos utilizados:
- IEEE 802.15.4 CLI
- OpenThread CLI y CoAP en ESP-IDF
- Border Router con ESP-IDF
- Sniffing 802.15.4

Ver [`doc/syllabus.md`](doc/syllabus.md) para el programa detallado de laboratorios y [`doc/labs_overview_8w.md`](doc/labs_overview_8w.md) para el plan semanal. Los ejercicios detallados están en `labs/`. Setup en `doc/setup.md`.
