# IoT Systems Design Course / Curso de Diseño de Sistemas IoT

**ESP32-C6 • OpenThread • ISO/IEC 30141:2024**

---

## 🇬🇧 English

### [📚 Start the Course →](en/)

**8 hands-on labs** building a Thread mesh IoT system, aligned with **ISO/IEC 30141:2024** standard.

**What you'll build:**
- Thread mesh sensor network
- CoAP application protocol
- Secure border router gateway
- Complete dashboard integration

**Technologies:** ESP32-C6, OpenThread, CoAP, CBOR, DTLS

---

### Quick Navigation (English)

| Document | Description |
|----------|-------------|
| [📖 Course Overview](en/README.md) | Start here - complete course introduction |
| [⚙️ Setup Guide](en/0_setup.md) | Install ESP-IDF and configure environment |
| [🎯 Project Scenario](en/1_project_scenario.md) | GreenField Technologies - your role as IoT engineer |
| [🏗️ ISO Architecture](en/2_iso_architecture.md) | ISO/IEC 30141:2024 reference architecture guide |
| [📝 Templates](en/3_deliverables_template.md) | DDR and ADR templates for deliverables |
| [🔍 Quick References](en/references.md) | CoAP, Thread, ESP-IDF cheat sheets |
| [🧪 Labs 1-8](en/labs/) | Weekly lab guides with role-based context |
| [📐 Detailed Guides](en/labs/implementacion/) | Step-by-step implementation references |

---

## 🇪🇸 Español

### [📚 Ir al Curso →](es/)

**8 laboratorios prácticos** construyendo un sistema IoT con redes mesh Thread, alineado con el estándar **ISO/IEC 30141:2024**.

**Lo que construirás:**
- Red de sensores mesh con Thread
- Protocolo de aplicación CoAP
- Gateway border router seguro
- Integración completa con dashboard

**Tecnologías:** ESP32-C6, OpenThread, CoAP, CBOR, DTLS

---

### Navegación Rápida (Español)

| Documento | Descripción |
|-----------|-------------|
| [📖 Vista General del Curso](es/README.md) | Empieza aquí - introducción completa |
| [⚙️ Guía de Instalación](es/0_preparacion.md) | Instalar ESP-IDF y configurar entorno |
| [🎯 Escenario del Proyecto](es/1_escenario_proyecto.md) | GreenField Technologies - tu rol como ingeniero IoT |
| [🏗️ Arquitectura ISO](es/2_arquitectura_iso.md) | Guía de arquitectura de referencia ISO/IEC 30141:2024 |
| [📝 Plantillas](es/3_plantilla_entregables.md) | Plantillas DDR y ADR para entregables |
| [🔍 Referencias Rápidas](es/referencias.md) | Hojas de referencia CoAP, Thread, ESP-IDF |
| [🧪 Labs 1-8](es/labs/) | Guías de laboratorio semanales con contexto de roles |
| [📐 Guías Detalladas](es/labs/implementacion/) | Referencias de implementación paso a paso |

---

## 📊 Course Structure / Estructura del Curso

```
Week/Semana 1-2:  Physical/Link Layer       →  SCD Domain
Week/Semana 3-4:  Mesh Network & CoAP       →  SCD + ASD Domains
Week/Semana 5-6:  Border Router & Security  →  SCD + OMD + RAID
Week/Semana 7-8:  Dashboard & Integration   →  All 6 ISO Domains
```

### ISO/IEC 30141:2024 Six Domains / Seis Dominios

| Domain / Dominio | Abbr. | Focus / Enfoque |
|------------------|-------|-----------------|
| Physical Entity | PED | Sensed/controlled objects / Objetos sensados/controlados |
| Sensing & Controlling | SCD | Sensors, actuators, gateways / Sensores, actuadores, gateways |
| Application & Service | ASD | Core functions, services / Funciones core, servicios |
| Operation & Management | OMD | Device lifecycle, monitoring / Ciclo de vida, monitoreo |
| User | UD | Human/digital users, HMI / Usuarios humanos/digitales, HMI |
| Resource Access & Interchange | RAID | Authentication, API / Autenticación, API |

---

## 🛠️ Tools / Herramientas

**Common tools for both languages / Herramientas comunes para ambos idiomas:**

| Tool | Description |
|------|-------------|
| [tools/coap_client.py](tools/coap_client.py) | CoAP client for testing |
| [tools/dashboard.py](tools/dashboard.py) | Simple dashboard server |
| [tools/ota_server.py](tools/ota_server.py) | OTA update server |
| [tools/test_e2e.py](tools/test_e2e.py) | End-to-end system tests |

---

## 📖 Reference / Referencia

**ISO/IEC 30141:2024 Standard:**
[ISO_IEC_30141_2024(en).pdf](ISO_IEC_30141_2024(en).pdf) - Internet of Things (IoT) Reference Architecture

---

## 🎓 What You'll Learn / Lo Que Aprenderás

✅ Design ISO-compliant IoT systems / Diseñar sistemas IoT compatibles con ISO
✅ Implement Thread mesh networks / Implementar redes mesh Thread
✅ Use CoAP protocol for constrained devices / Usar protocolo CoAP para dispositivos restringidos
✅ Secure IoT communications / Asegurar comunicaciones IoT
✅ Build complete sensor-to-dashboard systems / Construir sistemas completos sensor-a-dashboard
✅ Document architectural decisions / Documentar decisiones arquitectónicas

---

## 🚀 Getting Started / Comenzar

### English Course
1. Go to [en/](en/)
2. Read [en/README.md](en/README.md)
3. Follow [en/0_setup.md](en/0_setup.md)
4. Start [en/labs/lab1.md](en/labs/lab1.md)

### Curso en Español
1. Ir a [es/](es/)
2. Leer [es/README.md](es/README.md)
3. Seguir [es/0_preparacion.md](es/0_preparacion.md)
4. Comenzar [es/labs/lab1.md](es/labs/lab1.md)

---

## 📂 Repository Structure / Estructura del Repositorio

```
4201327-IoT_Systems_Design_Labs/
│
├── README.md                    (This file / Este archivo)
├── ISO_IEC_30141_2024(en).pdf  (Standard / Estándar)
│
├── en/                          🇬🇧 English Course
│   ├── README.md                   Course overview
│   ├── 0_setup.md                  Environment setup
│   ├── 1_project_scenario.md       GreenField project
│   ├── 2_iso_architecture.md       ISO/IEC 30141 guide
│   ├── 3_deliverables_template.md  DDR & ADR templates
│   ├── references.md               Quick references
│   └── labs/                       8 lab guides
│       ├── lab1.md - lab8.md
│       └── implementacion/         Detailed guides
│
├── es/                          🇪🇸 Curso en Español
│   ├── README.md                   Vista general del curso
│   ├── 0_preparacion.md            Instalación del entorno
│   ├── 1_escenario_proyecto.md     Proyecto GreenField
│   ├── 2_arquitectura_iso.md       Guía ISO/IEC 30141
│   ├── 3_plantilla_entregables.md  Plantillas DDR y ADR
│   ├── referencias.md              Referencias rápidas
│   └── labs/                       8 guías de laboratorio
│       ├── lab1.md - lab8.md
│       └── implementacion/         Guías detalladas
│
└── tools/                       🛠️ Utilities (language-agnostic)
    ├── coap_client.py
    ├── dashboard.py
    ├── ota_server.py
    └── test_e2e.py
```

---

**Ready to build professional IoT systems?**
**¿Listo para construir sistemas IoT profesionales?**

→ [English Course](en/) | [Curso en Español](es/)
