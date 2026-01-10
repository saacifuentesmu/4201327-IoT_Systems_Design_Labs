# Decision & Design Record (DDR)

> Keep this document alive. Update per lab.

## 1. Project Context
Brief system description (update after major labs).

---

## 2. Architecture Decision Records (ADRs)

### ADR-001: [Decision Title]
**Date:** YYYY-MM-DD | **Status:** Proposed/Accepted/Deprecated
**ISO/IEC 30141 Domain:** Device/Communication/Application/Information/Management

#### Context & Problem
What constraint or requirement drives this decision?

#### Decision
We will [solution] because [key reason].

#### Alternatives Considered
1. **Option A** - Rejected: [why]
2. **Option B** - Rejected: [why]

#### Consequences
- ✅ **Pros:** [benefits]
- ⚠️ **Cons:** [trade-offs/limitations]

---

## 3. Lab Evolution

| Lab | Objective | New Capabilities | Key Decisions |
|-----|-----------|------------------|---------------|
| 1-2 | Physical/Network Layer | 802.15.4, Thread mesh | |
| 3-4 | Application Layer | CoAP endpoints, sensors | |
| 5 | Gateway Integration | Border Router, Observe | |
| 6 | Security | OTA, secure boot | |
| 7-8 | Operations | Metrics, testing | |

---

## 4. First Principles Reflections

**Lab X: [Topic]**

**Why?** Answer the fundamental "why" questions:
- Why does [technology X] use [approach Y]?
- What physical/mathematical principle drives this design?

**Example:**
- Lab 1: *Why does 802.15.4 use O-QPSK modulation?*
- Lab 3: *Why does CoAP use UDP instead of TCP?*
- Lab 6: *Why is RSA-2048 preferred over RSA-1024?*

---

## 5. Experimental Log

### Experiment: [Hypothesis Being Tested]
**Date:** YYYY-MM-DD

**Hypothesis:** I expect [X] to happen because [theory].

**Setup:**
- Nodes: X
- Config: [key parameters]

**Results:**

| Metric | Expected | Measured | Δ | Analysis |
|--------|----------|----------|---|----------|
| Latency | 50ms | 75ms | +50% | Higher due to... |
| PER | 1% | 5% | +400% | Interference from... |

**Conclusion:** Hypothesis [supported/rejected]. Root cause: [explanation].

---

## 6. ISO/IEC 30141 Architectural Mapping

### Lab-to-Domain Mapping

| My Component | ISO Domain | Functional Unit | Justification |
|--------------|------------|-----------------|---------------|
| ESP32-C6 | Device | Sensing + Processing | Edge computation |
| Thread Stack | Communication | Routing + Forwarding | Mesh networking |
| CoAP Server | Application | Application Support | RESTful API |
| JSON encoder | Information Handling | Data Formatting | Serialization |

**Architectural Pattern:** [Gateway/Pub-Sub/Client-Server/etc.]

---

## 7. Performance Baselines

| Metric | Target | Measured | Status |
|--------|--------|----------|--------|
| RSSI @ 10m | > -70 dBm | _____ dBm | ✅/⚠️/❌ |
| CoAP latency | < 100 ms | _____ ms | ✅/⚠️/❌ |
| Battery life | > 6 months | _____ days | ✅/⚠️/❌ |
| Cache hit rate | > 70% | _____ % | ✅/⚠️/❌ |

---

## 8. Energy Budget (Lab 4+)

**Target:** 1 year on 2xAA batteries (2500 mAh total)

| State | Current | Duty Cycle | Avg Contribution |
|-------|---------|------------|------------------|
| Active (TX/RX) | _____ mA | _____% | _____ mA |
| Light sleep | _____ mA | _____% | _____ mA |
| Deep sleep | _____ mA | _____% | _____ mA |
| **Average** | | **100%** | **_____ mA** |

**Battery Life:** 2500 mAh / _____ mA = _____ hours = _____ days

**Optimization Ideas:**
- [ ] Reduce TX power if range permits
- [ ] Increase sleep duration
- [ ] Implement deep sleep (< 5 mA)

---

## 9. Security (Lab 6+)

**Threat Model (STRIDE):**

| Threat | Attack Vector | Asset at Risk | Mitigation | Status |
|--------|---------------|---------------|------------|--------|
| Spoofing | Fake OTA server | Firmware integrity | RSA-2048 signing | ✅ |
| Tampering | Modified binary | Code execution | Hash verification | ✅ |
| DoS | Flood requests | Availability | Rate limiting | ⚠️ |

---

## 10. Backlog / Future Work

- [ ] Optimize [X] for better [Y]
- [ ] Add [feature] if time permits
- [ ] Investigate [issue] root cause

---

## 11. Version History

| Date | Change | Lab |
|------|--------|-----|
| YYYY-MM-DD | Initial creation | Lab 1 |
| YYYY-MM-DD | Added ADR-001 (CoAP choice) | Lab 3 |
