# Curso de IoT - Fundamentos Prácticos

## Resumen del Curso

Este es un curso práctico de 8 semanas centrado en los **fundamentos de IoT** usando ejemplos reales con ESP-IDF. Utiliza ESP32-C6 DevKitC y OpenThread como herramientas prácticas para explorar conceptos clave de IoT: conectividad mesh, protocolos de aplicación, gestión de energía, y sistemas distribuidos.

### Metodología de Aprendizaje
El curso progresa a través de fases estructuradas:
- **Labs 1-2**: Fundamentos de Thread y CoAP
- **Labs 3-4**: Redes mesh y patrones de comunicación
- **Labs 5-6**: Sensores, seguridad y OTA
- **Labs 7-8**: Observabilidad y consolidación

### ¿Por qué estas herramientas?
- **ESP32-C6**: SoC moderno con múltiples radios (WiFi, BLE, 802.15.4)
- **ESP-IDF**: Framework oficial de Espressif para ESP32, con soporte completo para Thread
- **OpenThread**: Implementación open-source de Thread (protocolo usado en Matter/Google)

Estas herramientas permiten explorar conceptos IoT reales sin la complejidad de implementar protocolos desde cero.

## Documentación del Curso

- 📋 **[Programa Detallado](doc/syllabus.md)** - Cronograma semanal y objetivos de aprendizaje
- ⚙️ **[Configuración del Entorno](doc/setup.md)** - Guía completa de instalación (Windows nativo, Python, VS Code Extension + ESP‑IDF)
- 🧪 **[Laboratorios](labs/)** - **8 laboratorios** prácticos paso a paso

## Objetivos de Aprendizaje IoT
- Arquitecturas de sistemas IoT distribuidos
- Protocolos de comunicación para dispositivos constreñidos
- Gestión de energía en dispositivos embebidos
- Interoperabilidad y escalabilidad en redes mesh
- Seguridad en sistemas IoT
- Integración con infrastructure cloud/edge

## Herramientas y Tecnologías
**Tecnologías base:** ESP-IDF, OpenThread, ESP32-C6
**Por qué estas herramientas:**
- **ESP-IDF**: Framework oficial de Espressif, con soporte completo para Thread
- **OpenThread**: Implementación open-source de Thread (usado en Matter/Google)
- **ESP32-C6**: SoC moderno con múltiples radios (WiFi, BLE, 802.15.4)

Estas herramientas permiten explorar conceptos IoT sin la complejidad de implementar protocolos desde cero.

## Prerrequisitos de software
- Host Windows 10/11
- ESP-IDF v5.1+ (con toolchain RISC-V)
- Python 3.8+, pip
- Git
- Opcional: Wireshark + disector 802.15.4 para sniffing

Configuración rápida (alto nivel)
1) Instalar Python y Git en Windows.
2) Instalar VS Code y la extensión ESP-IDF.
3) Usar la extensión para instalar ESP-IDF v5.1.
4) Verificar que la placa `esp32c6` esté soportada.

## Placas y ejemplos
Placa objetivo: `esp32c6`. Ver documentación de ESP-IDF para ESP32-C6.

Ejemplos utilizados:
- OpenThread CLI y CoAP en ESP-IDF
- Border Router con ESP-IDF
- Sniffing 802.15.4

## Flujo del curso (conceptos IoT)
**Labs 1-2 - Fundamentos:**
1) Thread CLI + CoAP Base → Formación de red Thread y recursos CoAP básicos
2) PHY + MAC + Sniffing → Análisis de tráfico 802.15.4 y ajustes de CCA

**Labs 3-4 - Redes y Comunicación:**
3) 6LoWPAN + Routing/Resiliencia → Direccionamiento IPv6 y resiliencia de red
4) Border Router + App Patterns → Border Router y patrones observe/pub-sub

**Labs 5-6 - Aplicaciones y Seguridad:**
5) Sensores + Dashboard Inicial → Integración de sensores y dashboard básico
6) Seguridad & OTA → Secure boot, firma y actualizaciones OTA

**Labs 7-8 - Optimización y Consolidación:**
7) Observabilidad & Optimización → Métricas, caching y optimización
8) Consolidación & Hardening → Testing E2E, performance y documentación

Ver `doc/labs_overview_8w.md` para resumen de labs y `labs/` para ejercicios detallados. Setup en `doc/setup.md`.
