# Curso de IoT - Fundamentos Prácticos

## Resumen del Curso

Este es un curso práctico de 12 semanas centrado en los **fundamentos de IoT** usando ejemplos reales con Zephyr RTOS. Utiliza ESP32-C6 DevKitC y OpenThread como herramientas prácticas para explorar conceptos clave de IoT: conectividad mesh, protocolos de aplicación, gestión de energía, y sistemas distribuidos.

### Metodología de Aprendizaje
El curso progresa a través de tres fases estructuradas:
- **Semanas 1-3**: Ejemplos base de Zephyr (shell, CoAP) para entender el ecosistema
- **Semanas 4-8**: Desarrollo de proyectos propios aplicando conceptos IoT
- **Semanas 9-12**: Integración completa con dashboard y aplicaciones reales

### ¿Por qué estas herramientas?
- **Zephyr RTOS**: Sistema operativo profesional para IoT, usado en producción
- **OpenThread**: Implementación open-source de Thread (protocolo usado en Matter/Google)  
- **ESP32-C6**: SoC moderno con múltiples radios (WiFi, BLE, 802.15.4)

Estas herramientas permiten explorar conceptos IoT reales sin la complejidad de implementar protocolos desde cero.

## Documentación del Curso

- 📋 **[Programa Detallado](doc/syllabus.md)** - Cronograma semanal y objetivos de aprendizaje
- ⚙️ **[Configuración del Entorno](doc/setup.md)** - Guía completa de instalación (WSL2, Python, Zephyr)
- 🧪 **[Laboratorios](labs/)** - 12 laboratorios prácticos paso a paso

## Objetivos de Aprendizaje IoT
- Arquitecturas de sistemas IoT distribuidos
- Protocolos de comunicación para dispositivos constreñidos
- Gestión de energía en dispositivos embebidos
- Interoperabilidad y escalabilidad en redes mesh
- Seguridad en sistemas IoT
- Integración con infrastructure cloud/edge

## Herramientas y Tecnologías
**Tecnologías base:** Zephyr RTOS, OpenThread, ESP32-C6
**Por qué estas herramientas:**
- **Zephyr**: RTOS profesional para IoT, usado en producción
- **OpenThread**: Implementación open-source de Thread (usado en Matter/Google)  
- **ESP32-C6**: SoC moderno con múltiples radios (WiFi, BLE, 802.15.4)

Estas herramientas permiten explorar conceptos IoT sin la complejidad de implementar protocolos desde cero.

## Prerrequisitos de software
- Host Linux (Ubuntu 22.04+ recomendado)
- Python venv para west + herramientas (recomendado). Activar el venv antes de usar west.
- Zephyr SDK (con toolchain RISC-V), west, y dependencias
- Python 3.10+, pip, y esptool/dfu-util según sea necesario (west instala esptool)
- Opcional: Docker para OTBR, Wireshark + disector 802.15.4

Configuración rápida (alto nivel)
1) Instalar prerrequisitos de Zephyr y SDK desde la documentación oficial.
2) Clonar el workspace de Zephyr (este repo ya está presente en este entorno).
3) Exportar env y verificar que la placa esté listada.

## Placas y ejemplos
Placa objetivo: `esp32c6_devkitc`. Ver definiciones en `zephyr/boards/espressif/esp32c6_devkitc/` y verifica con `west boards | grep esp32c6`.

Ejemplos de OpenThread utilizados:
- `samples/net/openthread/coap` — Cliente/servidor CoAP sobre Thread
- `samples/net/openthread/coprocessor` — Firmware RCP/NCP para OTBR
- `samples/net/openthread/border_router` — BR basado en Zephyr (alternativa a OTBR en Linux)

## Flujo del curso (conceptos IoT)
**Fase 1 - Fundamentos (Semanas 1-3):**
1) Ecosistema embebido + RTOS → *usando ejemplos Zephyr shell*
2) Conectividad inalámbrica + formación de redes → *usando openthread/shell*  
3) Protocolos de aplicación + arquitectura cliente-servidor → *usando openthread/coap*

**Fase 2 - Desarrollo Propio (Semanas 4-8):**
4) Capa física + análisis de tráfico → *proyectos custom con sniffing*
5) Operaciones MAC + eficiencia energética → *implementaciones propias*
6) Internetworking + direccionamiento → *proyectos con IPv6/6LoWPAN*
7) Tolerancia a fallos + escalabilidad → *sistemas distribuidos*
8) Observabilidad + métricas → *telemetría y monitoring*

**Fase 3 - Integración (Semanas 9-12):**
9) Patrones de comunicación avanzados → *publish/subscribe, observability*
10) Integración de sensores + edge computing → *aplicaciones end-to-end*
11) Seguridad IoT + actualizaciones OTA → *deployment seguro*
12) Sistemas completos + integración cloud → *dashboard y APIs*

Ver `doc/syllabus.md` para detalles por semana y `labs/` para ejercicios. Setup en `doc/setup.md`.

## Laboratorios
- Lab 01 — Ecosistema embebido y RTOS: `labs/lab01_setup_hello.md`
- Lab 02 — Conectividad inalámbrica y mesh (OpenThread CLI): `labs/lab02_openthread_cli.md`
- Lab 03 — CoAP sobre Thread: `labs/lab03_coap.md`
- Lab 04 — PHY 802.15.4 y sniffing: `labs/lab04_phy_sniffing.md`
- Lab 05 — Operaciones MAC 802.15.4: `labs/lab05_mac_ops.md`
- Lab 06 — 6LoWPAN e IPv6: `labs/lab06_6lowpan_ipv6.md`
- Lab 07 — Enrutamiento y resiliencia (MLE): `labs/lab07_routing_resilience.md`
- Lab 08 — Protocolos de aplicación (CoAP y MQTT‑SN): `labs/lab08_app_protocols.md`
- Lab 09 — Border Router (OTBR) con RCP ESP32‑C6: `labs/lab09_border_router.md`
- Lab 10 — Sensores y gestión de energía: `labs/lab10_sensors_power.md`
- Lab 11 — Seguridad y OTA (MCUboot): `labs/lab11_security_ota.md`
- Lab 12 — Dashboard mínimo: `labs/lab12_dashboard.md`
- Lab 12 (final) — Integración final y dashboard: `labs/lab12_final_dashboard.md`
