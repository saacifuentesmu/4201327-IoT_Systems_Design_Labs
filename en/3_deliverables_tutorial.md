# Design & Decision Record (DDR) - Annotated Guide
**GreenField Technologies | IoT Systems Design**

**Team Members:**
1. ____________________
2. ____________________

---

## 1. System Overview
*Update this section as your system evolves.*

*   **System Type:** [ ] Component (Lab 1-2) | [ ] System (Lab 3-6) | [ ] Environment (Lab 7-8)
*   **Description:** (1-2 sentences)

---

## 2. Lab Log & Stakeholder Summaries
*For each lab, summarize your work for the primary stakeholder.*

### Lab 1: RF Characterization
*   **To Samuel (Architect):** (e.g., Measured range, selected Channel X because...)
*   **To Maria (Ops):** (e.g., Interference report...)

### Lab 2: 6LoWPAN
*   **To Samuel:** (e.g., Latency measurements...)

### Lab 3: Thread & CoAP
*   **To Emma (Customer):** (e.g., Why battery life is better...)

### Lab 4: Sensors & Control
*   **To Maria:** (e.g., Reliability of downlink...)

### Lab 5: Border Router
*   **To Emma:** (e.g., Remote access status...)

### Lab 6: Security
*   **To Alex (Security):** (e.g., Threat model summary...)

### Lab 7: Dashboard
*   **To James (Product):** (e.g., Battery health monitoring...)

### Lab 8: Final Integration
*   **To All:** (e.g., Final system status...)

---

## 3. Architecture Decision Records (ADRs)
*Document key decisions. Copy this block for each new decision.*

**ADR-___: [Title]**
*   **Context:** (What was the problem?)
*   **Decision:** (What did you choose?)
*   **Rationale:** (Why? Reference ISO Domains/First Principles)
*   **Status:** [ ] Proposed | [ ] Accepted | [ ] Deprecated

*(Suggested ADRs: ADR-001 Channel Selection, ADR-002 Mesh Topology, ADR-003 CoAP vs HTTP, ADR-004 Polling Strategy, ADR-005 Security Mode)*

---

## 4. ISO/IEC 30141 Domain Mapping
*Map your components to the 6 Domains. Update continuously.*

| Component | ISO Domain | Justification |
|-----------|------------|---------------|
| Example: Soil Sensor | SCD | Sensing Entity |
| Example: Thread Mesh | SCD | Network Support |
| ... | ... | ... |

---

## 5. First Principles Reflections
*Answer the "Theory Questions" from each Lab Guide here.*

**Lab 1:**
1.  ...
2.  ...

**Lab 2:**
1.  ...

...

---

## 6. Performance Baselines
*Record your measured data against targets.*

| Metric | Target | Measured | Status |
|--------|--------|----------|--------|
| Lab 1: Max Range | > 20m | ___ m | [ ] Pass |
| Lab 2: Healing Time | < 120s | ___ s | [ ] Pass |
| Lab 3: CoAP Latency | < 200ms| ___ ms | [ ] Pass |
| Lab 4: Poll Latency | < 5s | ___ s | [ ] Pass |
| Lab 6: DTLS Time | < 3s | ___ s | [ ] Pass |

---

## 7. Ethics & Sustainability Checklist
*Review at each stage.*

*   [ ] **Lab 1:** Verified interference doesn't disrupt neighbors.
*   [ ] **Lab 4:** Data collection minimized (Privacy).
*   [ ] **Lab 5:** System works locally without cloud (Sustainability).
*   [ ] **Lab 6:** Encryption enabled (Privacy).
*   [ ] **Lab 8:** End-of-Life plan considered.