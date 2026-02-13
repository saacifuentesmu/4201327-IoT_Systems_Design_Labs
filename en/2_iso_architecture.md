# ISO/IEC 30141:2024 IoT Reference Architecture

This guide introduces the ISO/IEC 30141:2024 standard and explains how it applies to our IoT Systems Design course. Use this as a reference throughout the course.

**Contents:**
- What is ISO/IEC 30141 and why it matters
- Six viewpoints for analyzing IoT systems
- Six functional domains (PED, SCD, ASD, OMD, UD, RAID)
- How course labs map to the architecture
- Emergent characteristics of IoT systems

---

## Why Standards Matter in IoT

**Scenario**: You build an IoT system for a client.

**Without standards:**
- Client: "Where does authentication happen?"
- You: "Uh... in the code somewhere?"
- Client: "How do I integrate this with my existing infrastructure?"
- You: "Let me rebuild it to fit your needs..." 💸💸💸

**With standards:**
- Client: "Where does authentication happen?"
- You: "In the RAID (Resource Access & Interchange Domain), following ISO/IEC 30141 Section 8.7."
- Client: "Perfect, that matches our architecture. Ship it!" ✅

**Standards provide a common language** for architects, clients, and stakeholders.

---

## ISO/IEC 30141:2024 Overview

### What is ISO/IEC 30141?

**Full title**: *Internet of Things (IoT) — Reference Architecture*

**Published**: 2024 (revised from 2018 edition)
**Scope**: Describes architecture for IoT systems from multiple viewpoints
**Goal**: Common framework for designing, implementing, and documenting IoT systems

**Think of it as**: The architectural blueprint language for IoT, like UML is for software or architectural drawings are for buildings.

### Six Viewpoints (ISO/IEC 30141 Section 6)

The standard describes IoT systems from **six complementary viewpoints**:

```
┌────────────────────────────────────────────────────────────┐
│                  ISO/IEC 30141 VIEWPOINTS                  │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. FOUNDATIONAL      What is an IoT system?              │
│     - Concepts, definitions, characteristics              │
│                                                            │
│  2. BUSINESS          Why build this system?              │
│     - Value proposition, stakeholders, objectives         │
│                                                            │
│  3. USAGE             Who uses it and how?                │
│     - User roles, activities, interactions                │
│                                                            │
│  4. FUNCTIONAL        What does the system do?            │
│     - Functional components, data flows, domains          │
│                                                            │
│  5. TRUSTWORTHINESS   How do we ensure reliability?       │
│     - Security, privacy, safety, resilience               │
│                                                            │
│  6. CONSTRUCTION      How do we build and deploy it?      │
│     - Implementation patterns, deployment models          │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

**Key Insight**: Each viewpoint answers a different question. A complete architecture addresses **all six**.

### Why Six Viewpoints?

**Example**: Smart Agriculture System

**Viewpoint 1 - Foundational:**
- What is the system? A network of soil moisture sensors, irrigation actuators, and a control dashboard.

**Viewpoint 2 - Business:**
- Why? To reduce water usage by 30% while maintaining crop yield.
- Stakeholders: Farmers, agronomists, water utility companies.

**Viewpoint 3 - Usage:**
- Who? Farm manager (operator), agronomist (analyst), IT admin (administrator).
- How? Manager views dashboard, receives alerts, manually overrides automation.

**Viewpoint 4 - Functional:**
- Components: Sensors (SCD), irrigation controller (SCD), data analytics (ASD), dashboard (UD).
- Data flows: Sensor → Controller → Database → Dashboard.

**Viewpoint 5 - Trustworthiness:**
- Security: Encrypted communication (DTLS), authenticated OTA updates.
- Reliability: Mesh self-healing, redundant Border Routers.
- Safety: Fail-safe irrigation shutoff on sensor malfunction.

**Viewpoint 6 - Construction:**
- Implementation: ESP32-C6 devices, Thread mesh, CoAP protocol, Docker-based backend.
- Deployment: On-premises Border Router, cloud-hosted dashboard.

**Each viewpoint reveals different aspects.** Together, they form a complete picture.

---

## 3. Six Functional Domains
The **Functional Viewpoint** (Viewpoint 4) divides IoT systems into **six domains**.

### Visual Overview

```
┌───────────────────────────────────────────────────────────────┐
│         Physical Entity Domain (PED)                          │
│  Sensed objects: soil, air, water                             │
│  Controlled objects: pumps, lights, valves                    │
└───────────────────────────────────────────────────────────────┘
                            ↕ (Sensing/Actuation)
┌───────────────────────────────────────────────────────────────┐
│      Sensing & Controlling Domain (SCD)                       │
│  - Sensors, actuators, IoT gateways                           │
│  - Local control, protocol conversion                         │
│  - Example: ESP32-C6 devices, Thread Border Router            │
└───────────────────────────────────────────────────────────────┘
                            ↕ (Data/Commands)
┌───────────────────────────────────────────────────────────────┐
│      Application & Service Domain (ASD)                       │
│  - Core functions: data processing, storage, analytics        │
│  - Basic services: identity, inventory, geolocation           │
│  - Business logic: irrigation scheduler, anomaly detection    │
└───────────────────────────────────────────────────────────────┘
                            ↕ (Management)
┌───────────────────────────────────────────────────────────────┐
│      Operation & Management Domain (OMD)                      │
│  - OSS: Device lifecycle, monitoring, compliance              │
│  - BSS: Customer management, billing (if applicable)          │
└───────────────────────────────────────────────────────────────┘
                            ↕ (User Interaction)
┌───────────────────────────────────────────────────────────────┐
│             User Domain (UD)                                  │
│  - Human users: Admin, operator, viewer                       │
│  - Digital users: External systems, APIs                      │
│  - HMI: Web dashboard, mobile app, voice interface            │
└───────────────────────────────────────────────────────────────┘
                            ↔ (Authentication, API Exposure)
┌───────────────────────────────────────────────────────────────┐
│      Resource Access & Interchange Domain (RAID)              │
│  - Access management: Authentication, authorization           │
│  - Interchange: API exposure, capability publication          │
└───────────────────────────────────────────────────────────────┘
```

### Domain Details

#### PED - Physical Entity Domain

**Definition**: Physical objects that are sensed or controlled by the IoT system.

**Key Entities**:
- **Sensed physical objects**: Things you measure (temperature, humidity, motion)
- **Controlled physical objects**: Things you control (motors, lights, valves)

**Examples**:
- Smart home: Room temperature (sensed), thermostat setpoint (controlled)
- Agriculture: Soil moisture (sensed), irrigation pump (controlled)
- Industry: Machine vibration (sensed), conveyor belt speed (controlled)

**Important**: PED is NOT part of the IoT system—it's the **environment** the system operates in.

---

#### SCD - Sensing & Controlling Domain

**Definition**: Devices that interface with the physical world. The "edge" of the IoT system.

**Key Components**:
- **Sensors**: Acquire information from physical entities
- **Actuators**: Change properties of physical entities
- **IoT Gateways**: Connect SCD to other domains (protocol conversion, data aggregation)
- **Local control systems**: Run control loops without cloud connectivity

**Functions** (ISO/IEC 30141 Section 8.3):
- Sensing and actuation
- Protocol conversion (e.g., Thread → WiFi)
- Address mapping (e.g., MAC → IPv6)
- Data processing (e.g., filtering, aggregation)
- Security enforcement (e.g., firewall at gateway)

**In Our Course**:
- ESP32-C6 devices: Sensors, actuators
- Thread Border Router: IoT gateway
- Labs 1-2, 5: Focus on SCD

**Example**: ESP32-C6 reads temperature sensor (ADC) → Formats as CoAP message → Sends via Thread mesh → Border Router converts to WiFi → Forwards to cloud.

---

#### ASD - Application & Service Domain

**Definition**: Core functions and services that deliver IoT system functionality to users.

**Key Components**:
- **Basic services**: Data access, storage, processing, fusion
- **Business services**: Application-specific logic (e.g., irrigation scheduler)
- **Application hosting**: Platform for running IoT applications

**Functions**:
- Data storage (databases, time-series storage)
- Data processing (filtering, aggregation, analytics)
- Business logic (rules engine, decision making)
- Application APIs (REST, GraphQL, CoAP)

**In Our Course**:
- CoAP server: Application-layer protocol
- Data processing: JSON/CBOR parsing, validation
- Dashboard backend: Business logic
- Labs 3-4, 7: Focus on ASD

**Example**: CoAP server receives sensor data → Stores in time-series database → Runs analytics (detect anomalies) → Triggers alert if threshold exceeded.

---

#### OMD - Operation & Management Domain

**Definition**: Components responsible for managing devices and system operation.

**Key Components**:
- **OSS (Operational Support System)**:
  - Device lifecycle management (provisioning, decommissioning)
  - Monitoring and alerting
  - Compliance checking
  - Firmware updates (OTA)

- **BSS (Business Support System)** (if applicable):
  - Customer relationship management (CRM)
  - Subscription management
  - Billing and payment

**In Our Course**:
- OTA updates: OSS function (device lifecycle)
- Monitoring: Dashboard showing device health
- Labs 6-8: Focus on OMD

**Example**: OTA service detects new firmware version → Schedules update during low-traffic hours → Downloads to device → Verifies signature → Reboots → Confirms successful boot → Logs event.

---

#### UD - User Domain

**Definition**: Human and digital users interacting with the IoT system.

**Key Components**:
- **Human users**: People with specific roles (admin, operator, viewer)
- **Digital users**: Other systems/devices accessing IoT capabilities
- **HMI subsystem**: User interface (web, mobile, voice)

**User Roles** (vary by system):
| Role | Permissions | Example |
|------|-------------|---------|
| Administrator | Full control, configuration | IT staff |
| Operator | Monitoring, limited control | Factory supervisor |
| Viewer | Read-only access | Data analyst |
| Digital User | API access (OAuth) | External system integration |

**In Our Course**:
- Web dashboard: HMI for human users
- REST API: Interface for digital users
- Labs 7-8: Focus on UD

**Example**: Farm manager (human user) logs into dashboard → Views sensor readings → Clicks "Irrigate Zone 3" → UD sends command to ASD → ASD forwards to SCD → Actuator activates pump.

---

#### RAID - Resource Access & Interchange Domain

**Definition**: Controls access to IoT system resources and exposes capabilities to external systems.

**Key Components**:
- **Access management**: Authentication (who are you?), authorization (what can you do?)
- **Interchange subsystem**: Expose APIs, data, services to external parties
- **Reverse access management**: IoT system accessing partner systems

**Functions**:
- User/device authentication (certificates, OAuth, API keys)
- Role-based access control (RBAC)
- API gateway (rate limiting, throttling)
- API documentation (OpenAPI, Swagger)

**In Our Course**:
- CoAP authentication: Access management
- Resource discovery (/.well-known/core): API exposure
- Labs 4, 6, 8: RAID aspects

**Example**: External analytics platform requests data → RAID authenticates API key → Checks authorization (does this key have read access?) → If yes, forward to ASD → Return data → Log access.

---

### Domain Interaction Example

**Scenario**: User wants to turn on a pump remotely.

```
1. UD: User clicks "Turn On Pump" in dashboard
2. RAID: Authenticate user, check authorization (is user allowed?)
3. ASD: Business logic validates (is it safe to turn on pump? Not already on?)
4. SCD: Send CoAP PUT to actuator device
5. PED: Actuator turns on physical pump
6. SCD: Send confirmation back to ASD
7. ASD: Update database (pump state = ON)
8. UD: Dashboard updates button (Pump: ON ✅)
9. OMD: Log event (User X turned on Pump Y at Time Z)

Data flows through all six domains in ~200-500 ms.
```

---

## 4. Mapping to Course Labs
### Lab Progression and Domain Focus

| Lab | Title | Primary Domains | What You Build |
|-----|-------|-----------------|----------------|
| **Lab 1** | IEEE 802.15.4 Physical Layer | SCD | ESP32-C6 radio communication |
| **Lab 2** | 6LoWPAN & IPv6 | SCD | IPv6 over constrained networks |
| **Lab 3** | Thread Mesh Networking | SCD, ASD | Self-healing mesh |
| **Lab 4** | CoAP Application Protocol | ASD, RAID | RESTful API for IoT |
| **Lab 5** | Thread Border Router | SCD, RAID | Gateway connecting domains |
| **Lab 6** | Security & OTA | OMD, RAID | Device lifecycle management |
| **Lab 7** | Dashboard | UD, ASD | Human-machine interface |
| **Lab 8** | Integration | **All** | Complete system |

### Visual: Course as Architecture Construction

```
Week 1-2: Build the Foundation (SCD - Physical/Link layers)
    ┌─────────────────────────────────────┐
    │         IEEE 802.15.4 Radio         │
    │         6LoWPAN Compression         │
    └─────────────────────────────────────┘

Week 3-4: Add Connectivity (SCD, ASD - Networking)
    ┌─────────────────────────────────────┐
    │         Thread Mesh Network         │
    │         CoAP Application            │
    └─────────────────────────────────────┘

Week 5-6: Connect to World (SCD, OMD, RAID - Gateway, Security)
    ┌─────────────────────────────────────┐
    │        Border Router (Gateway)      │
    │        Security & OTA Updates       │
    └─────────────────────────────────────┘

Week 7-8: Complete System (UD, All domains - Integration)
    ┌─────────────────────────────────────┐
    │       Dashboard (User Interface)    │
    │      End-to-End Integration         │
    └─────────────────────────────────────┘

By Week 8, you have a complete ISO/IEC 30141-compliant system!
```

### Progressive Learning: From Components to Systems

**Lab 1-2**: IoT **Component** (single device)
- One ESP32-C6 device
- Understands: SCD basics

**Lab 3-5**: IoT **System** (multiple interacting components)
- Multiple Thread devices + Border Router
- Understands: SCD, ASD, RAID interactions

**Lab 6-8**: IoT **Environment** (complete operational system)
- Full stack: Sensors → Mesh → Gateway → Backend → Dashboard
- Understands: All six domains

**ISO/IEC 30141 Hierarchy**:
```
IoT Component → IoT System → IoT Environment
 (Lab 1-2)       (Lab 3-5)       (Lab 6-8)
```

---

## 5. Emergent Characteristics
### What Makes IoT Systems Special?

ISO/IEC 30141 Section 7 defines **emergent characteristics** — properties that arise from the system as a whole, not individual components.

| Characteristic | Definition | Course Example |
|----------------|------------|----------------|
| **Composability** | Components combine into larger systems | ESP32-C6 + Border Router + Dashboard = Complete system |
| **Heterogeneity** | Diverse devices, protocols, data formats | Thread + WiFi, CoAP + HTTP, CBOR + JSON |
| **Modularity** | Independent modules with defined interfaces | Each CoAP resource is independent |
| **Scalability** | System grows without architectural change | Add more Thread devices without reconfiguring |
| **Network communication** | Distributed components communicate | All devices exchange data via mesh |
| **Shareability** | Resources shared among multiple users | Multiple dashboard users access same sensors |
| **Accuracy** | Data quality and reliability | Sensor calibration, error detection |
| **Autonomy** | Self-management without human intervention | Mesh self-healing, automatic OTA rollback |
| **Manageability** | Remote monitoring and control | Dashboard, OTA updates |

### Example: Scalability

**Non-scalable design** (star topology):
```
All devices connect to central hub.
Add 100th device → Hub overloaded → System breaks.
```

**Scalable design** (mesh topology):
```
Devices form mesh with distributed routing.
Add 100th device → Mesh grows, no single bottleneck.
(Thread supports up to 511 devices per network)
```

**Thread is inherently scalable** due to mesh architecture.

### Example: Autonomy

**Non-autonomous**:
```
Router fails → Network down → Human must manually reconfigure all devices.
```

**Autonomous** (Thread):
```
Router fails → Mesh detects failure (30s) → Self-heals (re-routes) → No human intervention needed.
```

**ISO/IEC 30141 emphasizes systems that manage themselves.**

---

## 6. Q&A and Course Expectations
### Course Deliverables

1. **DDR (Decision & Design Record)**: Living document tracking your architectural decisions
   - Maps each lab to ISO/IEC 30141 domains
   - Documents design choices (ADRs)
   - Records performance measurements
   - See [3_deliverables_template.md](3_deliverables_template.md)

2. **ADRs (Architecture Decision Records)**: Integrated into DDR template
   - Example: "Why CoAP instead of MQTT?"
   - See ADR section in deliverables template

3. **Lab Implementations**: Working code for each lab
   - Must meet performance baselines (see [references.md](references.md) for performance targets)

4. **Final Integration** (Lab 8): Complete system demonstrating all six domains

### Assessment Rubric (High-Level)

| Component | Weight | Focus |
|-----------|--------|-------|
| **Lab Implementations** | 50% | Does it work? Meets performance targets? |
| **DDR Quality** | 30% | Architectural thinking, ISO mapping, ADRs |
| **Final Integration** | 15% | End-to-end system, failure mode analysis |
| **Participation** | 5% | Engagement, helping peers |

**Key**: We assess **architectural understanding**, not just coding ability.

### Study Resources

- **ISO/IEC 30141:2024 Standard**: [ISO_IEC_30141_2024(en).pdf](../ISO_IEC_30141_2024(en).pdf) (focus on Sections 6-8)
- **Quick References**: [references.md](references.md) — CoAP, Thread, ESP-IDF cheat sheets and performance baselines
- **Project Scenario**: [1_project_scenario.md](1_project_scenario.md) — GreenField Technologies context
- **Lab Guides**: [labs/](labs/) — 8 role-based lab guides with integrated theory

### Common Questions

**Q: Do I need to memorize all six domains?**
A: No, but you should understand what each domain does and be able to map your work to the correct domain(s).

**Q: Will we use all six domains in every lab?**
A: No. Labs 1-2 focus mainly on SCD. Later labs progressively add more domains. Lab 8 covers all six.

**Q: Is this course more theory or practical?**
A: **Both**. You'll build working systems (practical) while understanding **why** they work (theory). The theory preambles (10-15 min each lab) explain first principles.

**Q: What if I'm not familiar with networking concepts?**
A: That's okay! We start with basics (IEEE 802.15.4) and progressively build up. Review [references.md](references.md) if you need a refresher.

**Q: How much time should I expect to spend per lab?**
A: ~6-8 hours per lab (2-3 hours in class, 4-5 hours outside). Labs 6-8 may take longer (10-12 hours).

---

## Homework Assignment (Due Next Week)

### Part 1: Read ISO/IEC 30141 Excerpts
- Section 6: Reference Architecture (Viewpoints)
- Section 8.3: Sensing & Controlling Domain (SCD)
- **Goal**: Familiarize yourself with standard terminology

### Part 2: Multi-Viewpoint Analysis of a Real IoT System

Choose one of these IoT systems:
- Smart home (Nest, HomeKit, etc.)
- Wearable fitness tracker (Fitbit, Apple Watch)
- Industrial monitoring (factory sensors)
- Smart city (traffic lights, parking)

**Task A**: Create a diagram mapping components to the **six domains** (PED, SCD, ASD, OMD, UD, RAID).

**Task B**: Analyze the system from **three viewpoints**:

| Viewpoint | What to Document |
|-----------|------------------|
| **Foundational** | What is the system? What are its boundaries? What emergent characteristics does it have (autonomy, scalability, etc.)? |
| **Functional** | How do the six domains interact? Draw a data flow diagram showing how information moves through the system. |
| **Usage** | Who are the users? What are their roles? Describe one typical user workflow step-by-step. |

**Example (Fitbit System)**:

**Domains**:
```
PED: User's heart, steps, calories burned
SCD: Fitbit device (sensors: accelerometer, heart rate monitor; BLE radio)
ASD: Fitbit cloud (data processing, activity recognition, calorie calculation)
OMD: Firmware updates, device pairing, health data compliance (HIPAA)
UD: Fitbit mobile app (HMI)
RAID: OAuth login, API for third-party apps (MyFitnessPal, Strava)
```

**Viewpoint Analysis**:

*Foundational*: "The Fitbit system is a wearable health monitoring platform. Characteristics: (1) Autonomy - automatically detects activities without user input; (2) Shareability - data shared across multiple apps via API; (3) Accuracy - calibrated sensors for reliable health metrics."

*Functional*: "Data flow: PED (user's heartbeat) → SCD (heart rate sensor) → BLE → Mobile app (ASD local processing) → Cloud (ASD analytics) → UD (app displays heart rate graph). Commands flow reverse: UD (user sets alarm) → Cloud (ASD) → BLE → SCD (device vibrates)."

*Usage*: "Primary user role: Health-conscious individual. Workflow: (1) Morning: User checks sleep score on app (UD query to ASD); (2) During exercise: Device records heart rate (SCD to ASD); (3) Post-workout: User reviews workout summary, shares to social media (UD to RAID to external system)."

**Submission**: 1-2 pages with diagram + three viewpoint analyses (300-400 words total)

### Part 3: Set Up Development Environment
- Install ESP-IDF v5.1+
- Verify ESP32-C6 board detected
- Flash "hello world" example
- See [0_setup.md](0_setup.md) for instructions

---

## Summary

### Key Takeaways

1. ✅ **ISO/IEC 30141** provides a common language for IoT architecture
2. ✅ **Six viewpoints** answer different questions (what, why, who, how, security, deployment)
3. ✅ **Six domains** organize functional components (PED, SCD, ASD, OMD, UD, RAID)
4. ✅ **Course labs** progressively build a complete ISO-compliant system
5. ✅ **Emergent characteristics** (scalability, autonomy, etc.) distinguish IoT from traditional embedded systems

### Looking Ahead

**Next Week (Lab 1)**:
- IEEE 802.15.4 physical layer
- SCD domain focus
- First-principles: Why O-QPSK modulation? Link budget calculations.
- **Bring**: ESP32-C6 board, USB cable, laptop with ESP-IDF installed

---

---

**End of ISO/IEC 30141 Guide**
