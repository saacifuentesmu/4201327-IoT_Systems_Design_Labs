# IoT Systems Design Course

**Start Here** | ESP32-C6 • OpenThread • ISO/IEC 30141:2024

---

## Welcome!

This course trains **IoT Systems Architects**, not just embedded developers. Over 8 labs, you'll build a complete Thread mesh network system while learning the ISO/IEC 30141:2024 reference architecture.

### What Makes This Course Different?

| Traditional Embedded Course | This Course |
|-----------------------------|-------------|
| "Make it blink" | "Why does it work this way?" |
| Copy-paste code | Understand first principles |
| Lab reports | Professional architecture documentation |
| Individual components | Complete system integration |

---

## 🚀 Getting Started

### Week 0: Preparation

**1. Set Up Your Environment**
→ Follow [0_setup.md](0_setup.md) to install ESP-IDF and VS Code

**2. Understand the Project Context**
→ Read [1_project_scenario.md](1_project_scenario.md) - You'll work at **GreenField Technologies**

**3. Learn the Architecture Framework**
→ Review [2_iso_architecture.md](2_iso_architecture.md) - ISO/IEC 30141:2024 overview

---

## 📚 Course Structure

### The Project: GreenField Technologies

Throughout the course, you're a **Junior IoT Systems Engineer** at GreenField Technologies, developing a soil monitoring network for small farms.

**Your team:**
- **You & Your Partner** (Labs 1-6) / **Team of 4** (Labs 7-8)
- **Eng. Samuel Cifuentes** (Instructor) - Senior Architect reviewing your work
- **Stakeholders** - Product Owner, Field Operations, Security Lead, Pilot Customer

**Team Structure:**
- **Labs 1-6**: Work in **pairs** (2 students per team)
  - Share 2× ESP32-C6 development boards
  - Maintain one shared DDR document
  - Alternate driver/navigator roles weekly

- **Labs 7-8**: Merge into **teams of 4** (2 pairs combine)
  - Build larger mesh network (4+ nodes)
  - Integrate different subsystems
  - Combine architectural knowledge for system-level design

**Project phases:**

| Labs | Phase | What You Build |
|------|-------|---------------|
| **1-2** | Feasibility Study | RF characterization, IPv6 networking |
| **3-4** | Network Design | Thread mesh, CoAP application protocol |
| **5-6** | Integration & Security | Border router, encryption, OTA updates |
| **7-8** | Deployment | Dashboard, complete system integration |

### The 8 Labs

Each lab includes:
- ✅ **Project context** - Email from stakeholders with this week's mission
- ✅ **Theory** - First-principles explanations (the "why")
- ✅ **Tasks** - Hands-on implementation
- ✅ **Deliverables** - DDR updates, performance measurements

**Lab guides:** [labs/](labs/)

| Lab | Title | ISO Domains | What You Learn |
|-----|-------|-------------|---------------|
| [Lab 1](labs/lab1.md) | RF Characterization | SCD | IEEE 802.15.4 radio, link budgets |
| [Lab 2](labs/lab2.md) | 6LoWPAN & IPv6 | SCD | IP over constrained networks |
| [Lab 3](labs/lab3.md) | CoAP & CBOR | ASD | Efficient data transport |
| [Lab 4](labs/lab4.md) | Sensor Integration | ASD, SCD | Complete sensor-to-cloud path |
| [Lab 5](labs/lab5.md) | Border Router | SCD, RAID | Gateway between domains |
| [Lab 6](labs/lab6.md) | Security & OTA | OMD, RAID | Encryption, firmware updates |
| [Lab 7](labs/lab7.md) | Dashboard | UD, ASD | User interface, visualization |
| [Lab 8](labs/lab8.md) | System Integration | **All 6** | Complete ISO-compliant system |

**Need more technical details?** Each lab has a detailed implementation guide in [labs/implementation/](labs/implementation/)

---

## 📖 Course Materials

### Core Documents (Read These)

1. **[0_setup.md](0_setup.md)** - Environment setup guide
2. **[1_project_scenario.md](1_project_scenario.md)** - GreenField Technologies project briefing
3. **[2_iso_architecture.md](2_iso_architecture.md)** - ISO/IEC 30141:2024 architecture guide
4. **[3_deliverables_template.md](3_deliverables_template.md)** - DDR and ADR templates
5. **[4_ethics_sustainability.md](4_ethics_sustainability.md)** - Privacy, compliance, and sustainable design
6. **[5_theory_foundations.md](5_theory_foundations.md)** - First-principles theory (the "why")
7. **[references.md](references.md)** - Quick reference cheat sheets (bookmark this!)

### Lab Materials

- **[labs/](labs/)** - 8 role-based lab guides (start here each week)
- **[labs/implementation/](labs/implementation/)** - Detailed technical guides (reference when stuck)

---

## 🎯 What You'll Deliver

Instead of traditional lab reports, you produce **professional engineering artifacts**:

### 1. Design Decision Record (DDR)
A living document tracking your architectural decisions, updated each lab.
- Maps work to ISO/IEC 30141 domains (PED, SCD, ASD, OMD, UD, RAID)
- Documents design choices (ADRs)
- Records performance measurements

**Template:** [3_deliverables_template.md](3_deliverables_template.md)

### 2. Architecture Decision Records (ADRs)
Standalone justifications for major technical decisions.
- Example: "Why CoAP instead of MQTT?"
- Includes alternatives considered, tradeoffs, consequences

### 3. Performance Reports
Verification that your system meets operational requirements.
- Example: "Mesh healing time < 60s"
- Baselines in [references.md](references.md)

### 4. Stakeholder Summaries
Different audiences care about different aspects:
- **Samuel (Architect)**: Technical depth, ISO alignment
- **James (Product)**: Cost, performance, business value
- **Maria (Operations)**: Deployment, troubleshooting
- **Alex (Security)**: Threat mitigation, compliance

---

## 🏗️ ISO/IEC 30141:2024 Architecture

The course is built around the ISO/IEC 30141:2024 IoT Reference Architecture.

### Six Functional Domains

Your system spans six functional domains:

```
PED (Physical Entity Domain)
  ↕ Sensing/Actuation
SCD (Sensing & Controlling Domain) ← Labs 1-2, 5
  ↕ Data/Commands
ASD (Application & Service Domain) ← Labs 3-4, 7-8
  ↕ Management
OMD (Operation & Management Domain) ← Labs 6-8
  ↕ User Interaction
UD (User Domain) ← Labs 7-8
  ↔ Auth/API
RAID (Resource Access & Interchange) ← Labs 4, 6
```

### Six Viewpoints

You'll analyze your system from six complementary viewpoints:

| Viewpoint | Question | Labs |
|-----------|----------|------|
| **Foundational** | What is an IoT system? | 1-2 |
| **Business** | Why build this? | 8 |
| **Usage** | Who uses it and how? | 7 |
| **Functional** | What does it do? | 1-8 |
| **Trustworthiness** | How is it secure? | 6, 8 |
| **Construction** | How do we build it? | 1-8 |

**Learn more:** [2_iso_architecture.md](2_iso_architecture.md)

---

## 🛠️ Technology Stack

- **Hardware**: ESP32-C6 DevKitC
- **Framework**: ESP-IDF v5.1+
- **Networking**: OpenThread (Thread mesh protocol)
- **Application**: CoAP (Constrained Application Protocol)
- **Data Format**: CBOR (Compact Binary Object Representation)
- **Security**: DTLS, AES-128-CCM

---

## 📊 Assessment

| Component | Weight | What's Assessed |
|-----------|--------|-----------------|
| **Lab Implementations** | 50% | Does it work? Meets performance baselines? |
| **DDR Quality** | 30% | Architectural thinking, ISO mapping, ADRs |
| **Final Integration** | 15% | End-to-end system, all six domains working |
| **Participation** | 5% | Engagement, helping peers, asking good questions |

**We assess architectural understanding, not just coding ability.**

---

## 🎓 Learning Outcomes

By the end of this course, you will:

✅ **Design** ISO/IEC 30141-compliant IoT systems
✅ **Implement** Thread mesh networks with CoAP
✅ **Document** architectural decisions professionally (ADRs)
✅ **Analyze** systems from multiple viewpoints
✅ **Troubleshoot** distributed IoT systems
✅ **Communicate** technical decisions to diverse stakeholders
✅ **Build** a portfolio-worthy complete IoT system
✅ **Consider** ethical implications: privacy, sustainability, compliance

---

## 📅 Week-by-Week Guide

### Week 0: Preparation
- [ ] Install ESP-IDF ([0_setup.md](0_setup.md))
- [ ] Read project scenario ([1_project_scenario.md](1_project_scenario.md))
- [ ] Review ISO architecture ([2_iso_architecture.md](2_iso_architecture.md))
- [ ] Understand ethics & sustainability ([4_ethics_sustainability.md](4_ethics_sustainability.md))

### Week 1: Lab 1 - RF Characterization
- [ ] Read [labs/lab1.md](labs/lab1.md)
- [ ] Complete RF measurements
- [ ] Update DDR with Lab 1 findings
- [ ] Submit ADR-001 (channel selection)

### Week 2-8: Continue through labs
- Follow the pattern: Read lab → Complete tasks → Update DDR → Submit ADRs

### Week 8: Final Integration
- Complete system spanning all six domains
- Final DDR with all six viewpoints analyzed
- Demonstrate working system

---

## 💡 Tips for Success

1. **Read ahead**: Review next week's lab before class
2. **Use references**: Bookmark [references.md](references.md) for quick lookups
3. **Document as you go**: Update your DDR immediately after each lab
4. **Think like an architect**: Always ask "why?" not just "how?"
5. **Engage with stakeholders**: Frame your work in terms of stakeholder concerns
6. **Test thoroughly**: Meet all performance baselines before moving on

---

## 🆘 Need Help?

- **Quick lookup**: [references.md](references.md) - CoAP, Thread, ESP-IDF commands
- **Theory deep-dive**: [5_theory_foundations.md](5_theory_foundations.md) - First-principles explanations
- **Detailed implementation**: [labs/implementation/](labs/implementation/) - Step-by-step guides
- **ISO questions**: [2_iso_architecture.md](2_iso_architecture.md) - Architecture reference
- **Project context**: [1_project_scenario.md](1_project_scenario.md) - Stakeholder profiles
- **Ethics & compliance**: [4_ethics_sustainability.md](4_ethics_sustainability.md) - Privacy, GDPR, sustainability

---

## 🌟 What's Next?

**Ready to start?**

1. → [0_setup.md](0_setup.md) - Set up your development environment
2. → [1_project_scenario.md](1_project_scenario.md) - Meet your team at GreenField
3. → [2_iso_architecture.md](2_iso_architecture.md) - Learn the ISO/IEC 30141 framework
4. → [labs/lab1.md](labs/lab1.md) - Begin Lab 1!

**Good luck, and welcome to the team!**

---

_This course is based on ISO/IEC 30141:2024 "Internet of Things (IoT) — Reference Architecture"_
