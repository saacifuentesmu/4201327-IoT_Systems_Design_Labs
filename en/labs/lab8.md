# Lab 8: Capstone Integration (The "Golden Master")
> **Technical Guide:** [SOP-08: Consolidation & Hardening](sops/sop08_consolidation.md)

**GreenField Technologies - SoilSense Project**
**Phase:** Production Release
**Duration:** 2 Weeks (Final Sprint)
**ISO Domains:** All Domains (System View)

---

## 1. Project Context

### Your Mission This Week

**From:** Samuel Cifuentes (Senior Architect)
**To:** Firmware Team
**Subject:** FIELD DEPLOYMENT GO/NO-GO

This is it. GreenField has the pilot deployment scheduled for next Monday.
We need the **Golden Master (v1.0)** firmware.

**The Exam:**
I will take your binary. I will flash it to 3 nodes in the lab.
I will run the "Chaos Script":
1.  Cut power to the Border Router.
2.  Jam the WiFi.
3.  Flood the network with traffic.
4.  Reboot the nodes randomly.

**If your system survives and recovers automatically, you pass.**
If I have to press the "Reset" button even once, we fail the pilot.

Good luck.

— Samuel

---\

### Stakeholders Counting On You

| Stakeholder | Their Question | How This Lab Helps |
|---|---|---|
| **Everyone** | "Does it actually work?" | This is the Final Acceptance Test (FAT). |

---

## 2. The Final Checklist (ISO 30141 Viewpoints)

Before you submit `soilsense_v1.bin`, verify your **DDR**:

### System View (Lab 1 & 5)
* [ ] Does the Radio connect reliably?
* [ ] Does it reach the Cloud?

### Functional View (Lab 2 & 4)
* [ ] Does the Mesh heal if a router dies?
* [ ] Do actuators work even after sleeping?

### Usage View (Lab 3 & 7)
* [ ] Is the data CBOR compressed?
* [ ] Can we see Battery levels?

### Trustworthiness View (Lab 6)
* [ ] Is DTLS encryption enabled?
* [ ] Are threats mitigated?

---

## 3. The Stress Test (Self-Audit)

Perform these tests yourself before submitting:

1.  **The "Cold Start":** Remove all batteries. Insert them. Does the network form in < 2 minutes?
2.  **The "Blackout":** Turn off the Border Router for 10 minutes. Turn it on. Do nodes reconnect?
3.  **The "Long Haul":** Leave it running overnight. Are there 0 crashes?

---

## 4. Deliverables (The Final Package)

1.  **Binary:** `soilsense_v1.bin`
2.  **DDR Final Version:** Complete history of all 8 labs.
3.  **Video Demo:** A 2-minute video showing:
    * Sensor heating up (Data change).
    * Dashboard updating.
    * Node disconnection & recovery.
4.  **Ethics Assessment:** Completed Section 11 of your DDR.

---

## 5. Final Ethics Assessment

*Reference: [4_ethics_sustainability.md](../4_ethics_sustainability.md)*

Before declaring your system production-ready, complete this ethical review:

### System-Level Ethics Checklist

**Privacy & Data**
- [ ] We documented exactly what data SoilSense collects (DDR Section 11)
- [ ] Emma can access all her data
- [ ] Emma can delete her data if she leaves the service
- [ ] Data retention period is defined and justified

**Sustainability**
- [ ] System works without cloud (local-first via Border Router)
- [ ] ESP32-C6 can be repurposed after project ends
- [ ] OTA updates extend device lifespan (not planned obsolescence)
- [ ] Open protocols (Thread/CoAP) prevent vendor lock-in

**Stakeholder Impact**
- [ ] We considered who could be harmed if system is misused
- [ ] We have mitigations for identified risks

### Final Reflection (Include in DDR)

**Answer these questions in your DDR Section 11:**

1. If GreenField Technologies shuts down in 5 years, will Emma's sensors still work? How?

2. What data could we stop collecting without losing core functionality?

3. Who benefits from this system? Who might be disadvantaged?

4. What would you do differently if you rebuilt this system with ethics as a primary requirement from day one?

---

**Congratulations. You are now an IoT Systems Architect.**

You've built a complete system spanning all six ISO/IEC 30141 domains, and you understand that engineering excellence includes ethical responsibility.

*"The best engineers build systems that not only work, but that they would be proud to explain to anyone affected by them."*