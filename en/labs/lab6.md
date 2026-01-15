# Lab 6: Security & Trustworthiness
> **Technical Guide:** [SOP-06: Security & OTA](sops/sop06_security_ota.md)

**GreenField Technologies - SoilSense Project**
**Phase:** Hardening
**Duration:** 3 hours
**ISO Domains:** RAID (Resource Access), Trustworthiness (Cross-cutting)

---

## 1. Project Context

### Your Mission This Week

**From:** Sebastian (Security Lead)
**To:** Firmware Team
**Subject:** VULNERABILITY DETECTED

I ran a penetration test on the Pilot Farm network. **It failed.**

I was able to:
1.  Sniff the air and read the exact temperature values (Privacy violation).
2.  Inject a fake packet telling the irrigation valve to "OPEN", flooding Daniela's greenhouse.

**This is a critical stop-ship issue.**
We need **Defense in Depth**. You must implement **DTLS (Datagram Transport Layer Security)** to encrypt the CoAP links.

— Sebastian

### Stakeholders Counting On You

| Stakeholder | Their Question | How This Lab Helps |
|---|---|---|
| **Sebastian (Security)** | "Can an attacker inject fake commands?" | DTLS provides Integrity and Authentication. |
| **Daniela (Farmer)** | "Is my farm data private?" | Encryption ensures Confidentiality. |
| **ISO 30141 Auditor** | "Have you addressed Trustworthiness?" | You are implementing the **Trustworthiness Viewpoint**. |

---

## ISO/IEC 30141 Context

### Visual Domain Mapping

```mermaid
graph TD
    subgraph Trustworthiness [Trustworthiness Viewpoint]
        Confidentiality[Encryption (DTLS)]
        Integrity[Message Integrity]
        Availability[DoS Protection]
    end
    subgraph RAID [Communication]
        Client --"Encrypted Channel (DTLS)"--> Server
    end
    Confidentiality -.-> Client
    Integrity -.-> Server
    
    style Trustworthiness fill:#f9f,stroke:#333,stroke-width:2px
    style RAID fill:#bbf,stroke:#333,stroke-width:2px
```

---

## 2. Theory Preamble (15 min)
*Reference: [Theory Foundations](../5_theory_foundations.md) > Lab 6: Security & Trustworthiness*

* **STRIDE Model:** Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation of Privilege.
* **The Cost of Security:** A DTLS handshake requires ~6 flights of packets. It is "expensive" in energy. We must minimize how often we handshake.

---

## 3. Execution Tasks

### Task A: The Threat Model (Paper Exercise)
Before coding, go to your DDR. Fill out the **STRIDE Table**.
* *Scenario:* "Attacker with a laptop standing 50m from the greenhouse."
* *Identify:* 3 specific threats.

### Task B: DTLS Implementation (Pre-Shared Key)
Upgrade your CoAP server to **CoAPS** (Port 5684).
* **Key Management:** Use a hardcoded PSK (for lab only). In production, this would be in the Secure Element.
* **Test:** Attempt to read data with a standard CoAP client (Should timeout/fail).
* **Test:** Read data with a CoAPS client and the correct Key (Should succeed).

### Task C: Packet Sniffing
Use the Sniffer.
* **Observe:** The payload should now be "Encrypted Application Data" (Gibberish).

---

## 4. Deliverables (Update your DDR)

* **Threat Model:** The completed STRIDE table.
* **Performance Check:** Measure the time to complete a DTLS handshake. Is it `< 3 seconds`?
* **ADR-006 (Encryption):** Rationale for using Pre-Shared Keys vs. Certificates (Constraint: Flash size and complexity).

---

## 5. Ethics Connection: Privacy Through Security

*Reference: [4_ethics_sustainability.md](../4_ethics_sustainability.md)*

Security is the technical foundation of privacy. Your DTLS implementation protects Daniela's data from:

| Threat | Without DTLS | With DTLS |
|--------|-------------|-----------|
| **Eavesdropping** | Competitor reads soil moisture data | Encrypted - unreadable |
| **Tampering** | Attacker sends fake "irrigate" command | Authenticated - rejected |
| **Data inference** | Patterns reveal farm operations | Protected during transit |

### Reflection Questions (for your DDR Section 11)

1. **Data minimization**: Now that we encrypt data, should we also reduce *what* we collect?
2. **Regulatory compliance**: How does DTLS help us meet GDPR's "security of processing" requirement?
3. **User transparency**: Does Daniela know her data is encrypted? Should she?

**Remember**: Encryption protects data *in transit*. Consider: Is Daniela's data also encrypted *at rest* on the dashboard server?

---

## Grading Rubric (Total: 100 points)

### Technical Execution (40 points)
* [ ] CoAPS (DTLS) server running on port 5684 (15 pts)
* [ ] Handshake successful with PSK (10 pts)
* [ ] Packet sniffing verifies payload is encrypted (15 pts)

### ISO/IEC 30141 Alignment (30 points)
* [ ] Trustworthiness Viewpoint addressed (15 pts)
* [ ] Threat Model (STRIDE) completed (15 pts)

### Analysis (20 points)
* [ ] ADR-006 (Encryption) justification (10 pts)
* [ ] Handshake latency measurement (10 pts)

### Ethics Checkpoint (Mandatory Pass/Fail)
* [ ] **Privacy**: Encryption enabled (Privacy protection).
* [ ] **Transparency**: Did you document the security limitations (e.g., PSK management) so stakeholders are aware?
