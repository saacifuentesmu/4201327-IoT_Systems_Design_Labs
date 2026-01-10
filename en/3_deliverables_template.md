# Course Deliverables Template

This template contains all deliverables for the IoT Systems Design course:
1. **Decision & Design Record (DDR)** - Your living architecture document
2. **Architecture Decision Records (ADRs)** - Specific technical decisions
3. **Stakeholder Communication** - Summaries for different audiences

> **Living Document**: Update this DDR throughout the course as your system evolves.

---

# Decision & Design Record (DDR) - ISO/IEC 30141:2024

---

## 1. Project Context

### Team Information

**Team Members** (Labs 1-6 - Pair):
- **Student 1**: [Your Full Name]
- **Student 2**: [Partner's Full Name]

**Team Name** (Optional): [e.g., "Thread Warriors", "Mesh Masters", etc.]

**Merged Team** (Labs 7-8 - Team of 4):
- **Pair 1**: [Names from above]
- **Pair 2**: [Partner Pair Names]

**Course**: IoT Systems Design
**Instructor**: Eng. Samuel Cifuentes
**Semester**: [e.g., Spring 2026]

---

### System Overview
Brief description of your IoT system (update after major labs).

**Smart Agriculture Example:**
> This system monitors soil moisture, temperature, and light levels in a greenhouse environment. It controls irrigation pumps and grow lights based on sensor data. The system uses ESP32-C6 devices in a Thread mesh network, with a Border Router connecting to a cloud dashboard.

### ISO/IEC 30141:2024 Architectural Context

**Primary ISO Domains Used:**
- [ ] **PED** (Physical Entity Domain) - Sensed/controlled objects
- [ ] **SCD** (Sensing and Controlling Domain) - Sensors, actuators, gateways
- [ ] **ASD** (Application and Service Domain) - Core functions, services
- [ ] **OMD** (Operation and Management Domain) - Device management, monitoring
- [ ] **UD** (User Domain) - Human/digital users, HMI
- [ ] **RAID** (Resource Access and Interchange Domain) - Auth, API exposure

**System Type** (check one):
- [ ] IoT Component (single device)
- [ ] IoT System (multiple interacting components)
- [ ] IoT Environment (multiple systems)

**Viewpoint Focus** (primary viewpoint for current lab phase):
- [ ] Foundational (concepts, characteristics)
- [ ] Business (value, stakeholders)
- [ ] Usage (user roles, activities)
- [ ] Functional (domain interactions)
- [ ] Trustworthiness (security, reliability)
- [ ] Construction (deployment, patterns)

### Six Viewpoint Analysis

Document how your system addresses each viewpoint. Update this progressively as you complete labs.

| Viewpoint | Key Questions | Your System's Answer | Lab(s) Covered |
|-----------|---------------|----------------------|----------------|
| **1. Foundational** | What is your IoT system? What are its boundaries and key characteristics? | *Example: A distributed sensor network with 10 ESP32-C6 nodes forming a Thread mesh. Characteristics: Self-healing (autonomy), scales to 100+ devices (scalability), heterogeneous protocols (Thread + WiFi).* | Labs 1-2 |
| **2. Business** | Why does this system exist? What value does it provide? Who are the stakeholders? | *Example: Reduces greenhouse water usage by 30% while maintaining crop yield. Stakeholders: Farm owner (cost savings), agronomist (data-driven decisions), maintenance technician (remote monitoring).* | Lab 7-8 |
| **3. Usage** | Who uses the system and how? What are the user roles and workflows? | *Example: Roles: (1) Administrator - configures devices, manages users; (2) Operator - monitors sensors, controls irrigation; (3) Viewer - analyzes historical data. Workflows documented in Lab 7.* | Lab 7 |
| **4. Functional** | What does the system do? How do functional domains interact? | *Example: SCD (sensors) → ASD (data processing) → UD (dashboard). CoAP for SCD↔ASD, WebSocket for ASD↔UD. Detailed domain mapping in Section 4 below.* | Labs 1-8 |
| **5. Trustworthiness** | How is the system secured? What are the failure modes and mitigation strategies? | *Example: DTLS for communication, RSA-2048 for OTA signatures, certificate-based authentication. Mesh self-heals in <60s after node failure. Threat model in Section 9 below.* | Labs 6, 8 |
| **6. Construction** | How is the system built and deployed? What are the implementation patterns? | *Example: ESP32-C6 devices (SCD), Border Router (gateway pattern), Docker containers (backend). Deployment: On-premises BR, cloud-hosted dashboard. Details in Lab Evolution (Section 3).* | Labs 1-8 |

**Instructions**: Fill in the "Your System's Answer" column as you progress through labs. Reference specific sections of this DDR for details.

---

## 2. Stakeholder Communication Summary

*This section helps you communicate your design to different stakeholders at GreenField Technologies. Each stakeholder cares about different aspects of your system, corresponding to different ISO viewpoints.*

### For Eng. Samuel Cifuentes (Senior Architect)
**Viewpoints:** Functional, Construction, Trustworthiness
**What she needs to know:**
- [ ] Which ISO/IEC 30141 domains does this lab address?
- [ ] What architectural patterns are you using? (Reference Annex A)
- [ ] What are the key technical tradeoffs and how did you resolve them?
- [ ] Do your ADRs justify decisions with first-principles reasoning?

**Your summary for Samuel** (2-3 sentences, technical):
> *Example (Lab 3): I implemented OpenThread mesh networking (SCD domain) using the MLE protocol for neighbor discovery and RPL for routing. The network self-heals in <60s after router failure (measured baseline). Key tradeoff: Router role increases power consumption by 15mA but provides network resilience - documented in ADR-003.*

---

### For James Park (Product Owner)
**Viewpoints:** Business, Usage
**What he needs to know:**
- [ ] Does this meet the product requirements? (cost, performance, features)
- [ ] What value does this provide to customers?
- [ ] What are the risks to timeline or functionality?
- [ ] Are there any customer-facing features completed?

**Your summary for James** (2-3 sentences, business impact):
> *Example (Lab 6): I implemented DTLS encryption which adds 2KB RAM overhead per connection. This meets our security requirement for GDPR compliance. Tradeoff: Each TLS handshake costs ~500ms, so we cache sessions to minimize latency (user sees <100ms response time in dashboard).*

---

### For Maria Santos (Field Operations)
**Viewpoints:** Construction, Operational (OMD)
**What she needs to know:**
- [ ] How do I deploy/configure this in the field?
- [ ] What can go wrong and how do I diagnose it?
- [ ] Are there any environmental limitations? (temperature, range, power)
- [ ] What maintenance is required?

**Your summary for Maria** (2-3 sentences, operational):
> *Example (Lab 4): Devices auto-join the Thread network within 10s of power-on - no manual configuration needed. If a device shows solid red LED, check: (1) Channel mismatch, (2) Network key incorrect, (3) Interference from WiFi Ch 1/6/11 (see troubleshooting table in Section 11). Maximum range between nodes: 50m in dense vegetation, 100m line-of-sight.*

---

### For Alex Chen (Security Lead)
**Viewpoint:** Trustworthiness
**What he needs to know:**
- [ ] What is the attack surface?
- [ ] How is data protected in transit and at rest?
- [ ] How are devices authenticated?
- [ ] Is the implementation compliant with security standards?

**Your summary for Alex** (2-3 sentences, security focus):
> *Example (Lab 6): I implemented Thread security with AES-128-CCM encryption (IEEE 802.15.4 standard). Network key is provisioned via QR code scan (prevents over-the-air eavesdropping). Threat model: Protected against eavesdropping and replay attacks; vulnerable to physical device capture (mitigation: add secure boot in next phase, see ADR-006).*

---

### For Emma Larson (Pilot Customer - Farmer)
**Viewpoint:** Usage
**What she needs to know:**
- [ ] How do I use this system?
- [ ] What information will I see and what do I do with it?
- [ ] Is setup simple?
- [ ] Will this actually help me improve my farm operations?

**Your summary for Emma** (2-3 sentences, user-focused):
> *Example (Lab 7): Your dashboard shows real-time soil moisture for each field zone. When moisture drops below 30%, you'll receive a notification suggesting irrigation. Setup: Scan QR code on sensor box, place in field, done - no technical knowledge required.*

---

**Note**: You don't need to fill all stakeholder sections for every lab - focus on the stakeholders most relevant to that lab's scope. For example, Lab 1 (RF characterization) is primarily for Samuel and Maria; Lab 7 (dashboard) is primarily for James and Emma.

---

## 3. Architecture Decision Records (ADRs)

### ADR-001: [Decision Title]

**Date:** YYYY-MM-DD
**Status:** [Proposed / Accepted / Deprecated / Superseded]
**ISO/IEC 30141 Domain:** [PED / SCD / ASD / OMD / UD / RAID]
**Viewpoint:** [Foundational / Business / Usage / Functional / Trustworthiness / Construction]

#### Context & Problem
What constraint, requirement, or challenge drives this decision?

**Example (Lab 3):**
> We need to choose between CoAP and MQTT for application-layer communication. Devices have limited memory (400KB RAM) and operate on battery power. Network is lossy (5-10% packet error rate).

#### Decision
We will [solution] because [key reason].

**Example:**
> We will use CoAP over UDP because: (1) UDP overhead is 8 bytes vs TCP's 20+ bytes, (2) CoAP has built-in reliability with CON messages, (3) Resource model fits our sensor API design.

#### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| **MQTT-SN** | Standard pub/sub model | Requires broker (additional device) | Added complexity, single point of failure |
| **HTTP/REST** | Well-known | TCP overhead, TLS handshake cost | Too heavy for constrained devices |
| **Raw UDP** | Lowest overhead | No reliability, no standardization | Would reinvent CoAP features |

#### Consequences

**Positive:**
- ✅ Lower memory footprint (~50KB vs ~150KB for MQTT)
- ✅ Better energy efficiency (no persistent TCP connections)
- ✅ Native support in ESP-IDF and OpenThread

**Negative:**
- ⚠️ Less mature tooling compared to MQTT
- ⚠️ No built-in pub/sub (must implement Observe pattern)
- ⚠️ Team learning curve (less familiar than HTTP)

**Risk Mitigation:**
- Use ESP-IDF's libcoap implementation (well-tested)
- Create CoAP quick reference guide for team
- Start with simple GET/PUT, add Observe later

#### Performance Impact (Quantitative)
- Packet size: CoAP header 4 bytes + token ~8 bytes = ~12 bytes vs MQTT-SN ~15 bytes
- Latency: CON request/response ~50-100ms (measured in Lab 4)
- Energy: ~30mA @ 50ms = 1.5 mJ per request

#### ISO/IEC 30141 Mapping
- **Domain**: ASD (Application and Service Domain)
- **Architectural Pattern**: Request-Response (Section A.2.1 in standard)
- **Emergent Characteristics**: Modularity (REST resources), Shareability (multi-client access)

---

## 3. Lab Evolution

| Lab | ISO Domain | Objective | New Capabilities | Key Decisions (ADR #) |
|-----|------------|-----------|------------------|-----------------------|
| 1 | SCD | Physical Layer | IEEE 802.15.4 radio setup | ADR-001: Modulation choice |
| 2 | SCD | Link/Network | 6LoWPAN, IPv6 addressing | ADR-002: Address scheme |
| 3 | SCD, ASD | Mesh Network | Thread routing, multi-hop | ADR-003: Router vs End Device |
| 4 | ASD, RAID | Application | CoAP endpoints, sensors | ADR-004: Protocol selection |
| 5 | SCD, RAID | Gateway | Border Router, NAT64 | ADR-005: WiFi vs Ethernet |
| 6 | OMD, RAID | Security/OTA | Secure boot, MCUboot | ADR-006: OTA strategy |
| 7 | UD, ASD | Dashboard | Web UI, real-time data | ADR-007: WebSocket vs CoAP Observe |
| 8 | All | Integration | End-to-end testing | ADR-008: Deployment architecture |

**Current Phase**: Lab ___ (Week ___)

---

## 4. ISO/IEC 30141 Architectural Mapping

### Domain Mapping - Detailed

| My Component | ISO Domain | Sub-domain/Function | Standard Section | Justification |
|--------------|------------|---------------------|------------------|---------------|
| Soil moisture sensor | SCD | Sensor (sensed physical object interface) | Section 8.3 | Acquires information about PED |
| ESP32-C6 device | SCD | Sensing/Controlling device | Section 8.3 | Edge computation, local control |
| Thread stack | SCD | Communication (mesh routing) | Section 8.3 | Multi-hop networking in SCD |
| Border Router | SCD | IoT Gateway | Section 8.3 | Protocol conversion, security enforcement |
| CoAP server | ASD | Application Support | Section 8.4 | RESTful API for resource access |
| JSON serialization | ASD | Data formatting | Section 8.4 | Information encoding |
| OTA service | OMD | OSS (Operational Support System) | Section 8.5 | Device lifecycle management |
| Web dashboard | UD | HMI subsystem | Section 8.6 | Human user interface |
| Auth service | RAID | Access management | Section 8.7 | Authentication, authorization |

### Cross-Domain Data Flows

```
PED (Physical entities)
  ↕ [Sensing/Actuation]
SCD (ESP32-C6 devices, Border Router)
  ↕ [CoAP requests, Thread mesh]
ASD (Data processing, storage, applications)
  ↕ [Monitoring, OTA commands]
OMD (Device management, operational monitoring)
  ↕ [User queries, control commands]
UD (Dashboard, mobile apps)
  ↔ [Authentication, API exposure]
RAID (API gateway, auth service)
```

### Architectural Pattern
**Pattern Name:** [IoT Component Pattern / IoT System Pattern / Dynamic Service Composition / etc.]

**Reference:** ISO/IEC 30141:2024, Annex A, Section A.___

**Pattern Description:**
> Our system implements the [pattern name] where [description of how your system fits the pattern].

**Example (Lab 5 - Border Router):**
> Our system implements the **IoT Gateway Pattern** (Annex A.2.3) where the ESP32-C6 Border Router acts as a gateway between the Thread mesh (SCD) and the IP network (ASD/UD). It performs protocol conversion (Thread ↔ WiFi), address mapping (NAT64), and security enforcement.

### Emergent Characteristics Analysis

ISO/IEC 30141 Section 7 defines emergent characteristics. Evaluate your system:

| Characteristic | Definition | How Our System Exhibits This | Evidence/Metrics |
|----------------|------------|------------------------------|------------------|
| **Composability** | Components combine into larger systems | ESP32-C6 devices + Border Router + Dashboard form complete system | Lab 8 integration test |
| **Heterogeneity** | Diverse devices, protocols, data formats | Thread + WiFi, CoAP + HTTP, CBOR + JSON | Multiple protocol support |
| **Modularity** | Independent modules with defined interfaces | CoAP resources have clear URI structure | `/sensors/temp`, `/actuators/pump` |
| **Scalability** | System grows without architectural change | Can add Thread devices without reconfiguring mesh | Tested up to ___ nodes |
| **Network communication** | Distributed components communicate | All devices exchange data via Thread mesh | Network topology diagram |
| **Shareability** | Resources shared among multiple users | Multiple dashboard users access same CoAP resources | Concurrent access test |
| **Accuracy** | Data quality and reliability | Sensor calibration, error detection | ±0.5°C temperature accuracy |
| **Autonomy** | Self-management without human intervention | Mesh self-healing, automatic OTA rollback | Network partition recovery |
| **Manageability** | Remote monitoring and control | Dashboard shows device health, enables OTA updates | OMD capabilities |

---

## 5. First Principles Reflections

### Lab 1: Physical Layer (IEEE 802.15.4)

**Why does IEEE 802.15.4 use O-QPSK modulation?**

*Your analysis here:*
- O-QPSK (Offset Quadrature Phase Shift Keying) has constant envelope (amplitude doesn't vary)
- Constant envelope allows use of non-linear power amplifiers (more efficient)
- Energy efficiency is critical for battery-powered IoT devices
- Alternative (FSK) requires linear amplifiers with lower efficiency

**Link Budget Analysis:**
- TX power: ___ dBm
- Receiver sensitivity: ___ dBm
- Path loss @ 2.4 GHz, 10m: 20 log₁₀(10) + 20 log₁₀(2400) - 27.55 = ___ dB
- Fade margin: ___ dB
- **Link budget**: TX - Path Loss + Margin = ___ dB (✅ Positive = link closes)

### Lab 3: Application Layer (CoAP)

**Why does CoAP use UDP instead of TCP?**

*Your analysis here:*
- TCP handshake: 3 packets (SYN, SYN-ACK, ACK) before data transfer
- TCP state maintenance: ~2KB RAM per connection on constrained device
- UDP: Stateless, 8-byte header vs TCP's 20+ bytes
- CoAP implements reliability at application layer (CON messages) only when needed

**Trade-off Analysis:**
- **UDP + CoAP CON**: Reliability when needed, 12-byte overhead
- **TCP + HTTP**: Always reliable, 20+ byte overhead + state
- **Decision**: UDP for our use case (acceptable 5% packet loss, memory-constrained)

### Lab 6: Security

**Why use RSA-2048 for signing but AES-128 for encryption?**

*Your analysis here:*
- Asymmetric crypto (RSA): Computationally expensive, but enables non-repudiation (firmware signing)
- Symmetric crypto (AES): ~1000x faster, but requires shared secret
- RSA-2048 signature verification: ~___ ms on ESP32-C6
- AES-128 encryption: ~___ MB/s on ESP32-C6
- **Strategy**: RSA for authentication (infrequent), AES for bulk data (frequent)

**Cryptographic Cost Measurement:**

| Operation | Algorithm | Time (ms) | Energy (mJ) | Use Case |
|-----------|-----------|-----------|-------------|----------|
| Sign firmware | RSA-2048 | N/A (done on server) | N/A | OTA image signing |
| Verify signature | RSA-2048 | ___ ms | ___ mJ | Device validates OTA |
| Encrypt flash | AES-128 | ___ ms | ___ mJ | Protect stored data |
| DTLS handshake | ECDHE+AES | ___ ms | ___ mJ | Secure CoAP |

---

## 6. Experimental Log

### Experiment: [Hypothesis Being Tested]

**Date:** YYYY-MM-DD
**Lab:** ___
**ISO Domain Focus:** [PED / SCD / ASD / OMD / UD / RAID]

#### Hypothesis
I expect [X] to happen because [theory/principle].

**Example (Lab 3):**
> I expect packet loss to increase with mesh depth (number of hops) because each hop introduces additional queuing delay and potential for collision. According to Thread spec, max 32 routers should maintain <5% packet loss.

#### Setup
- **Topology:** ___ nodes, ___ hops maximum depth
- **Configuration:** TX power ___ dBm, channel ___, PAN ID ___
- **Tools:** `ot-cli`, sniffer, performance monitor

**Network Diagram:**
```
[Border Router] ←→ [Router 1] ←→ [Router 2] ←→ [End Device]
       0 hops        1 hop         2 hops        3 hops
```

#### Results

| Metric | Expected | Measured | Δ (%) | Analysis |
|--------|----------|----------|-------|----------|
| RSSI @ 1 hop | > -70 dBm | ___ dBm | | |
| RSSI @ 3 hops | > -70 dBm | ___ dBm | | |
| Latency @ 1 hop | ~50 ms | ___ ms | | |
| Latency @ 3 hops | ~150 ms | ___ ms | | |
| Packet loss @ 1 hop | <2% | ___% | | |
| Packet loss @ 3 hops | <5% | ___% | | |

**Observed Behavior:**
- [Describe what you observed]
- [Any unexpected results?]
- [Performance bottlenecks identified]

#### Root Cause Analysis
**Why did results differ from expectations?**

1. **Factor 1**: [e.g., RF interference from WiFi on same 2.4 GHz band]
   - **Evidence**: Sniffer shows competing traffic
   - **Impact**: +20ms average latency

2. **Factor 2**: [e.g., Router 2 had high CPU load]
   - **Evidence**: `ot-cli` counters show queue drops
   - **Impact**: 8% packet loss vs expected 5%

#### Conclusion
Hypothesis [supported / partially supported / rejected].

**Key Learnings:**
- [Lesson 1]
- [Lesson 2]

**Improvements for Next Iteration:**
- [ ] Use Thread channel ___ to avoid WiFi interference
- [ ] Reduce application-layer data rate to prevent router queue overflow
- [ ] Add flow control at CoAP layer

---

## 7. Performance Baselines

### ISO/IEC 30141 Trustworthiness Metrics

**Availability**: System uptime, MTBF (Mean Time Between Failures)
**Reliability**: Probability of successful operation
**Resilience**: Recovery time from failures

| Metric | Target | Measured | Status | Lab |
|--------|--------|----------|--------|-----|
| **SCD Domain** |
| RSSI @ 10m | > -70 dBm | ___ dBm | ✅/⚠️/❌ | Lab 1 |
| Packet Error Rate | < 5% | ___% | ✅/⚠️/❌ | Lab 1 |
| Mesh convergence time | < 30 s | ___ s | ✅/⚠️/❌ | Lab 3 |
| **ASD Domain** |
| CoAP latency (1 hop) | < 100 ms | ___ ms | ✅/⚠️/❌ | Lab 4 |
| CoAP latency (3 hops) | < 300 ms | ___ ms | ✅/⚠️/❌ | Lab 4 |
| Dashboard update rate | > 1 Hz | ___ Hz | ✅/⚠️/❌ | Lab 7 |
| **OMD Domain** |
| OTA update time | < 5 min | ___ min | ✅/⚠️/❌ | Lab 6 |
| Device discovery time | < 10 s | ___ s | ✅/⚠️/❌ | Lab 5 |
| **End-to-End** |
| Sensor-to-dashboard latency | < 500 ms | ___ ms | ✅/⚠️/❌ | Lab 8 |
| System availability | > 99% | ___% | ✅/⚠️/❌ | Lab 8 |

**Status Legend:**
- ✅ **Green**: Meets or exceeds target
- ⚠️ **Yellow**: Within 20% of target, acceptable with known limitations
- ❌ **Red**: Does not meet target, requires investigation/improvement

---

## 8. Energy Budget (Lab 4+)

### Target
- **Battery capacity**: 2x AA batteries = 2500 mAh @ 3.0V
- **Target lifetime**: ___ months
- **Allowable average current**: 2500 mAh / (24h × 30d × ___ months) = ___ mA

### Current Consumption Profile

| State | Current (mA) | Duty Cycle (%) | Avg Contribution (mA) | Notes |
|-------|--------------|----------------|-----------------------|-------|
| **Active TX** | ___ mA | ___% | ___ mA | Transmitting sensor data |
| **Active RX** | ___ mA | ___% | ___ mA | Receiving ACKs, listening |
| **CPU Active** | ___ mA | ___% | ___ mA | Processing, CoAP stack |
| **Light Sleep** | ___ mA | ___% | ___ mA | Between TX/RX cycles |
| **Deep Sleep** | ___ mA | ___% | ___ mA | Long-term idle |
| **Total** | | **100%** | **___ mA** | |

### Battery Life Calculation
```
Battery Life = Battery Capacity / Average Current
            = 2500 mAh / ___ mA
            = ___ hours
            = ___ days
            = ___ months
```

**Result**: [✅ Meets target / ⚠️ Close / ❌ Does not meet target]

### Energy Optimization Strategies

**Implemented:**
- [x] Reduce TX power from ___ dBm to ___ dBm (acceptable RSSI)
- [x] Increase sensor sampling interval to ___ seconds
- [x] Use Thread SED (Sleepy End Device) mode

**Potential (not yet implemented):**
- [ ] Implement deep sleep (< 5 µA) between samples
- [ ] Use RTC-only mode during sleep
- [ ] Reduce mesh poll interval from ___ s to ___ s
- [ ] Batch multiple sensor readings per transmission

**Trade-off Analysis:**
- Longer sleep → Lower energy, but higher latency
- Lower TX power → Lower energy, but reduced range/reliability
- Less frequent sampling → Lower energy, but miss transient events

---

## 9. Security Analysis (Lab 6+)

### Threat Model (STRIDE Framework)

| Threat Type | Attack Vector | Asset at Risk | Impact (H/M/L) | Mitigation | Verification | Status |
|-------------|---------------|---------------|----------------|------------|--------------|--------|
| **Spoofing** | Fake OTA server | Firmware integrity | H | RSA-2048 signature verification | Attempt to flash unsigned image | ✅ |
| **Tampering** | Modified binary | Code execution | H | Hash verification, secure boot | Flash corrupted image | ✅ |
| **Repudiation** | Deny malicious action | Audit trail | M | Signed logs, timestamps | Log tampering test | ⚠️ |
| **Info Disclosure** | Sniff cleartext | Sensor data | M | DTLS encryption (AES-128) | Wireshark capture | ✅ |
| **DoS** | Flood CoAP requests | Availability | M | Rate limiting (max ___ req/s) | Stress test with `coap-client` | ⚠️ |
| **Elevation of Privilege** | Exploit buffer overflow | Root access | H | Code review, stack canaries | Fuzzing test | ❌ |

**Status:** ✅ Implemented | ⚠️ Partial | ❌ Not implemented

### ISO/IEC 30141 Trustworthiness Aspects

**Section 9 Mapping:**

| Aspect | Definition | Our Implementation | Verification Method |
|--------|------------|-------------------|---------------------|
| **Confidentiality** | Data accessible only to authorized entities | DTLS for CoAP, flash encryption | Packet capture shows encrypted traffic |
| **Integrity** | Data/firmware has not been tampered with | SHA-256 hashes, RSA signatures | Modified image rejected at boot |
| **Availability** | System operational when needed | Mesh self-healing, OTA rollback | Network partition recovery test |
| **Reliability** | Consistent correct operation | Error detection, retry logic | 99.x% successful CoAP transactions |
| **Resilience** | Recovery from faults/attacks | Watchdog timer, fail-safe defaults | Crash recovery test |
| **Safety** | Does not cause harm | Input validation, bounds checking | Actuator limit enforcement |
| **Compliance** | Follows regulations/standards | ISO/IEC 30141 architecture, Thread spec | Certification (if applicable) |

### Security Verification Tests

**Test 1: Firmware Signature Verification**
- **Setup**: Build unsigned OTA image, attempt to flash
- **Expected**: Device rejects unsigned image, logs error
- **Result**: [✅ Pass / ❌ Fail]
- **Evidence**: Serial log showing "Signature verification failed"

**Test 2: DTLS Encryption**
- **Setup**: CoAP request with DTLS enabled, capture with Wireshark
- **Expected**: Payload is encrypted (unreadable in packet capture)
- **Result**: [✅ Pass / ❌ Fail]
- **Evidence**: Wireshark screenshot showing encrypted CoAP payload

**Test 3: DoS Resilience**
- **Setup**: Send 100 req/s to CoAP server (exceeds rate limit)
- **Expected**: Server drops excessive requests, maintains availability for legitimate clients
- **Result**: [✅ Pass / ⚠️ Partial / ❌ Fail]
- **Evidence**: Server responds to legitimate client within ___ ms during attack

---

## 10. Failure Mode Analysis (Lab 8)

### What Happens When... (Resilience Testing)

| Failure Scenario | ISO Domain | Expected Behavior | Actual Behavior | Recovery Time | Status |
|------------------|------------|-------------------|-----------------|---------------|--------|
| **Border Router crash** | SCD | Thread mesh isolated, no internet access | | ___ seconds | |
| **Router node battery depleted** | SCD | Mesh re-routes around failed node | | ___ seconds | |
| **Network partition** (2 separate meshes) | SCD | Leader election in each partition, merge when link restored | | ___ seconds | |
| **OTA update fails mid-transfer** | OMD | Rollback to previous firmware | | ___ seconds | |
| **CoAP server unresponsive** | ASD | Client retries, timeout after ___ seconds | | ___ seconds | |
| **Dashboard loses connection** | UD | Reconnect automatically, buffer missed data | | ___ seconds | |
| **Certificate expired** | RAID | Reject connections, alert user | | Immediate | |

**Resilience Metrics:**
- **MTBF** (Mean Time Between Failures): ___ hours
- **MTTR** (Mean Time To Recover): ___ seconds
- **Availability**: MTBF / (MTBF + MTTR) = ___%

---

## 11. Ethics & Sustainability Assessment

*Reference: [4_ethics_sustainability.md](4_ethics_sustainability.md)*

### Data Ethics Checklist

Evaluate your system's data practices. Update as you complete labs.

**Data Collection** (Labs 4, 7):
- [ ] We collect only data necessary for stated functionality
- [ ] Data granularity is appropriate (not excessive)
- [ ] Users understand what data is collected

**Data Storage & Access** (Labs 5, 6):
- [ ] Data storage location is documented
- [ ] Data retention period is defined
- [ ] Third-party access policies are clear
- [ ] Data is encrypted at rest

**User Agency** (Labs 7, 8):
- [ ] Users can access their data
- [ ] Users can delete their data
- [ ] Users can opt out of non-essential features
- [ ] Privacy controls are accessible

**Security = Privacy** (Lab 6):
- [ ] Data encrypted in transit (DTLS)
- [ ] Device authentication implemented
- [ ] OTA update mechanism secured

### Regulatory Compliance

| Regulation | Applicable? | How We Comply | Lab |
|------------|-------------|---------------|-----|
| **GDPR (EU)** | ☐ Yes / ☐ No | | Lab 6-8 |
| - Right to access | | [How users access their data] | |
| - Right to erasure | | [How data is deleted on request] | |
| - Data minimization | | [Why each data point is needed] | |
| **Ley 1581 (Colombia)** | ☐ Yes / ☐ No | | Lab 6-8 |
| - Prior consent | | [How consent is obtained] | |
| - Purpose limitation | | [Stated purpose of data collection] | |

### Sustainability Design

**Device Longevity:**
- [ ] System operates without cloud (local-first) — Border Router approach
- [ ] Open protocols used (Thread/CoAP, not proprietary)
- [ ] Firmware is updatable (OTA)
- [ ] Hardware is repairable/modular

**End-of-Life Planning:**
- [ ] ESP32-C6 can be repurposed after project
- [ ] No cloud lock-in (device works independently)
- [ ] Documentation enables future maintenance

**E-Waste Mitigation:**
| Decision | Impact | Implemented? |
|----------|--------|--------------|
| Local-first architecture | Device works if cloud dies | ☐ Yes / ☐ No |
| Standard protocols | No vendor lock-in | ☐ Yes / ☐ No |
| Open firmware | Community can maintain | ☐ Yes / ☐ No |
| Replaceable battery | Extends device life | ☐ N/A (dev kit) |

### Ethical Reflection

**For your final DDR (Lab 8), answer:**

1. **Data minimization**: What data do we collect that we could eliminate?
   > *Your answer:*

2. **User control**: If Emma wants to stop using SoilSense, can she delete all her data?
   > *Your answer:*

3. **Longevity**: If GreenField shuts down in 5 years, will Emma's sensors still work?
   > *Your answer:*

4. **Stakeholder impact**: Who could be harmed by this system if misused? How do we mitigate?
   > *Your answer:*

---

## 12. Backlog / Future Work

### Technical Debt
- [ ] Refactor CoAP handler to reduce cyclomatic complexity
- [ ] Add unit tests for JSON serialization
- [ ] Document Border Router failure recovery procedure

### Feature Enhancements
- [ ] Implement CoAP Block-wise transfer for large payloads (>1KB)
- [ ] Add MQTT bridge for cloud integration (Lab 8+)
- [ ] Create mobile app for UD (currently web-only)

### Performance Optimizations
- [ ] Profile and optimize deep sleep entry/exit time (target <10ms)
- [ ] Implement adaptive TX power based on RSSI feedback
- [ ] Use CBOR instead of JSON to reduce payload size by ~30%

### Security Improvements
- [ ] Add certificate rotation mechanism (RAID)
- [ ] Implement secure commissioning with QR codes
- [ ] Add intrusion detection for anomalous traffic patterns

### ISO/IEC 30141 Compliance
- [ ] Document complete system architecture per Section 6 (all viewpoints)
- [ ] Add BSS (Business Support System) for user management (currently only OSS)
- [ ] Implement reverse access management (IoT system accessing partner systems)

---

## 13. Lessons Learned

### What Worked Well
- [Specific technical decision that paid off]
- [Tool or process that improved productivity]
- [ISO/IEC 30141 mapping helped visualize system architecture]

### What Could Be Improved
- [Challenge encountered and proposed solution]
- [Assumption that turned out to be incorrect]
- [Area where more first-principles analysis would have helped]

### Advice for Future Students
- Start early with [specific task]
- Don't underestimate [specific complexity]
- Use [specific tool/technique] for [specific purpose]

---

## 14. Version History

| Date | Change | Lab | ADR # | Author |
|------|--------|-----|-------|--------|
| YYYY-MM-DD | Initial DDR creation | Lab 1 | - | [Your name] |
| YYYY-MM-DD | Added ISO domain mapping | Lab 2 | - | [Your name] |
| YYYY-MM-DD | ADR-001: CoAP protocol choice | Lab 4 | ADR-001 | [Your name] |
| YYYY-MM-DD | Energy budget analysis | Lab 4 | - | [Your name] |
| YYYY-MM-DD | Security threat model | Lab 6 | ADR-006 | [Your name] |
| YYYY-MM-DD | Failure mode analysis | Lab 8 | - | [Your name] |

---

## Appendix: References

### ISO/IEC 30141:2024 Sections
- **Section 6**: Reference Architecture (viewpoints)
- **Section 7**: Emergent Characteristics
- **Section 8**: Functional Domains (PED, SCD, ASD, OMD, UD, RAID)
- **Section 9**: Trustworthiness Aspects
- **Annex A**: Construction Patterns

### Course Materials
- [2_iso_architecture.md](2_iso_architecture.md) - ISO/IEC 30141 architecture guide
- [4_ethics_sustainability.md](4_ethics_sustainability.md) - Privacy, compliance, sustainability
- [5_theory_foundations.md](5_theory_foundations.md) - First-principles theory
- [references.md](references.md) - CoAP, Thread, ESP-IDF quick refs and performance baselines

### External Resources
- Thread Specification: https://www.threadgroup.org/
- CoAP RFC 7252: https://datatracker.ietf.org/doc/html/rfc7252
- ESP-IDF Documentation: https://docs.espressif.com/projects/esp-idf/
