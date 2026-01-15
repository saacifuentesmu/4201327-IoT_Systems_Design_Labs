# GreenField Technologies: Project Briefing

**Document Type**: Project Context & Stakeholder Guide

**Audience**: IoT Systems Engineers (Students)

**Purpose**: Provide realistic development scenario for ISO/IEC 30141-aligned learning

---

## 1. Company Background

**GreenField Technologies** is a fictional agricultural technology startup founded in 2025. The company's mission is to make precision agriculture accessible to small and medium-scale farms (5-50 hectares) through affordable IoT sensor networks.

### Company Profile
- **Founded**: 2025
- **Market**: Small-scale sustainable farms in temperate climates
- **Competitors**: Established players focus on large industrial farms; GreenField targets the underserved small farm market

### Core Values
1. **Affordability** - Solutions must cost <$50/node to be competitive
2. **Simplicity** - Farmers shouldn't need IT expertise to deploy systems
3. **Sustainability** - Low power consumption, multi-year battery life
4. **Resilience** - Systems must work in remote areas with limited connectivity

---

## 2. The Product: SoilSense Network

### Product Vision
A wireless mesh network of environmental sensors that helps farmers optimize irrigation, reduce water waste, and improve crop yields through data-driven decisions.

### Target Customer Profile
- **Farm size**: 5-50 hectares
- **Crops**: Vegetables, orchards, small-scale grains
- **Tech comfort**: Basic smartphone usage
- **Pain points**:
  - Over-irrigation wastes water and money
  - Under-irrigation reduces yields
  - No real-time visibility into soil conditions
  - Weather stations don't reflect microclimate variations

### Minimum Viable Product (MVP) Requirements
1. **10-node sensor network** monitoring soil moisture and temperature
2. **Self-forming mesh** - farmers just power on devices
3. **3-month battery life** on coin cells
5. **Mobile dashboard** showing current conditions and trends
6. **Alert system** for irrigation scheduling

---

## 3. Your Role: IoT Systems Engineer

### Position Description
You are a **Junior IoT Systems Engineer** on the product development team. Your primary responsibility is designing and implementing the sensor network firmware and architecture.

**Team Structure:**
- **Labs 1-6**: Work in **pairs** (2 students)
- **Labs 7-8**: Merge into **teams of 4** (2 pairs combine) for system integration

### Your Manager
**Eng. Samuel Cifuentes** (Senior IoT Architect)
- Electronics Engineer, IoT Expert
- Reviews your Architecture Decision Records (ADRs)
- Provides technical guidance during weekly check-ins
- Expects ISO/IEC 30141-aligned documentation
- Values first-principles understanding over "copy-paste" solutions

### Your Team
**Your Partner** (Labs 1-6) / **Your Team** (Labs 7-8)
- **Labs 1-6**: You work with ONE partner
  - Share 3× ESP32-C6 boards
  - Maintain one shared DDR
  - Alternate driver/navigator roles each week

- **Labs 7-8**: Two pairs merge into a team of 4
  - Build larger mesh network (6+ nodes)
  - Integrate different subsystems
  - Combine DDRs into system-level architecture

### Other Teams
**Fellow engineering teams** - Other student pairs/teams in the class
- Share knowledge during code reviews
- Collaborate on infrastructure (border router, cloud integration)
- Compare performance benchmarks

### Your Stakeholders (Viewpoint Owners)

| Stakeholder | Role | Primary Concern | Maps to Viewpoint |
|-------------|------|-----------------|-------------------|
| **Samuel** | Senior Architect | System correctness, maintainability | Functional, Construction |
| **Gustavo** | Product Owner | Customer value, cost targets | Business, Usage |
| **Edwin** | Field Operations Lead | Deployment ease, reliability | Operational (OMD), Trustworthiness |
| **Sebastian** | Security Lead | Data privacy, secure communication | Trustworthiness |
| **Daniela** | Customer (Pilot Farmer) | Ease of use, actionable insights | Usage |

---

## 4. Project Phases (Mapped to Labs)

### Phase 1: Feasibility & Prototyping (Labs 1-2)
**Context**: The hardware team selected ESP32-C6. You need to validate it works in real farm environments.

**Your Tasks**:
- Characterize the 802.15.4 radio performance (PED domain)
- Determine maximum node spacing for reliable communication
- Measure power consumption baseline

**Stakeholder Questions You'll Answer**:
- Samuel: "What's the link budget? Show me the RF propagation model."
- Gustavo: "Can we achieve 100m range between nodes with this hardware?"
- Edwin: "What happens if a farmer places a node behind a metal barn?"

**Deliverables**:
- DDR documenting RF characterization (System & Functional viewpoints)
- ADR: "Why we chose channel 15 for mesh operation"

---

### Phase 2: Network Architecture (Labs 3-4)
**Context**: Hardware is validated. Now design the mesh network topology and application protocol.

**Your Tasks**:
- Implement OpenThread mesh networking (SCD domain)
- Design CoAP API for sensor data retrieval (ASD domain)
- Test network healing behavior

**Stakeholder Questions You'll Answer**:
- Samuel: "How does the system behave when a router node fails?"
- Gustavo: "What's the worst-case latency from sensor to gateway?"
- Edwin: "How long does it take for the network to recover after power loss?"

**Key Decision Points**:
- ADR: "CoAP vs MQTT for constrained devices" (you'll justify CoAP)
- ADR: "Polling vs push for sensor updates"

**Deliverables**:
- DDR with sequence diagrams showing data flows (Functional viewpoint)
- Performance report: Network healing time, message latency
- ADRs for protocol choices

---

### Phase 3: Integration & Security (Labs 5-6)
**Context**: Pilot customer identified. Need cloud integration and data protection before field deployment.

**Your Tasks**:
- Implement border router for Internet connectivity (RAID domain)
- Add DTLS encryption for sensor data (Trustworthiness viewpoint)
- Design provisioning workflow

**Stakeholder Questions You'll Answer**:
- Sebastian: "How do we prevent sensor spoofing attacks?"
- Gustavo: "What's the cost of encryption on battery life?"
- Daniela (Farmer): "Do I need to configure WiFi credentials on every sensor?"

**Critical Concerns**:
- Edwin: "Farmers can't be expected to enter 32-character PSKs. How do we make provisioning simple?"
- Sebastian: "We need GDPR compliance for EU customers. Where is data stored?"

**Deliverables**:
- DDR covering RAID and OMD domains
- STRIDE threat model
- ADR: "Pre-shared keys vs certificate-based authentication"
- Provisioning workflow diagram (Usage viewpoint)

---

### Phase 4: Deployment Readiness (Labs 7-8)
**Context**: Pilot deployment scheduled in 4 weeks. Final integration and validation required.

**Your Tasks**:
- Integrate with cloud dashboard (UD domain)
- Implement complete sleep/wake cycle for 3-month battery life
- System-wide testing and documentation

**Stakeholder Questions You'll Answer**:
- Gustavo: "What's the total bill-of-materials cost per node?"
- Edwin: "What's our deployment checklist? What can go wrong in the field?"
- Daniela: "Can I see real-time soil moisture on my phone?"
- Samuel: "Provide a complete system architecture diagram with all six ISO domains"

**Final Deliverable**: **System Integration Report**
- All six viewpoints analyzed
- Complete domain mapping (PED → SCD → ASD → OMD → UD → RAID)
- Performance verification against all baselines
- Deployment runbook for field operations

---

## 5. Communication Norms

### Weekly "Design Reviews" (Lab Sessions)
- Present your progress to Samuel (instructor)
- Discuss architectural tradeoffs
- Receive feedback on ADRs and DDRs

### Documentation Standards
Samuel expects **professional engineering documentation**, not academic reports:
- Use ISO/IEC 30141 vocabulary
- Justify decisions with quantitative analysis when possible
- Acknowledge tradeoffs explicitly
- Reference first principles (physics, protocol RFCs, security best practices)

### Cross-Functional Communication
Different stakeholders care about different aspects of your design:

**To Samuel (Architect)**: Technical depth, correctness, standards alignment
- "The mesh routing algorithm uses Trickle timers (RFC 6206) to minimize control traffic..."

**To Gustavo (Product)**: Business impact, cost, performance
- "By using deep sleep, we extended battery life from 6 weeks to 14 weeks, meeting the 3-month target with margin..."

**To Edwin (Operations)**: Reliability, troubleshooting, deployment
- "If a node fails to join the network, check these 3 things in this order..."

**To Sebastian (Security)**: Threat mitigation, compliance
- "We use AES-128-CCM (aligned with Thread spec) providing both confidentiality and authenticity..."

---

## 6. Success Criteria

### Technical Excellence
- ✅ All performance baselines met (see [References](references.md))
- ✅ System passes integration testing
- ✅ Documentation complete and ISO-aligned

### Professional Growth
- ✅ Can articulate design decisions from multiple viewpoints
- ✅ Understands first-principles "why" behind protocols
- ✅ Produces industry-quality ADRs and DDRs

### Stakeholder Satisfaction
- ✅ Samuel approves your architecture
- ✅ Gustavo confirms product requirements met
- ✅ Edwin has clear deployment procedures
- ✅ Sebastian validates security implementation

---

## 7. Real-World Grounding

While GreenField Technologies is fictional, the scenario is grounded in reality:

### Realistic Constraints
- **Cost targets** based on actual IoT module pricing
- **Battery life calculations** using real ESP32-C6 power profiles
- **Network performance** validated against 802.15.4 physics
- **Security requirements** aligned with GDPR and industry standards

### Authentic Stakeholder Conflicts
- **Product vs Engineering**: "Can we ship without full encryption to save cost?"
- **Operations vs Engineering**: "Your 'elegant' design requires 5 CLI commands to provision each node!"
- **Security vs Usability**: "Pre-shared keys are secure but farmers will write them on sticky notes..."

### Professional Practices
- ADRs document decisions **before** implementation (not post-hoc justification)
- Baselines define "done" (not subjective assessment)
- Viewpoint analysis ensures all stakeholders are considered

---

## 8. Pedagogical Intent

### What This Scenario Adds
1. **Context for viewpoints**: Each viewpoint maps to a real stakeholder with distinct concerns
2. **Motivation for rigor**: Samuel (instructor) expects professional documentation because that's what industry requires
3. **Tradeoff awareness**: Stakeholder conflicts force you to balance competing requirements
4. **Portfolio value**: Deliverables resemble real work products

### What This Scenario Avoids
- ❌ High-pressure military/defense framing (Option 5 style)
- ❌ Abstract academic exercises disconnected from application
- ❌ Prescriptive "cookbook" instructions that discourage critical thinking
- ❌ Single-stakeholder perspective (typical student → instructor dynamic)

---

## 9. Using This Scenario in Class

- **Write DDRs to Samuel**, addressing his technical concerns
- **Consider all stakeholders** when making design decisions
- **Use professional language**: "I selected CoAP because..." vs "I had to use CoAP for the assignment"
- **Build a portfolio**: These documents showcase your work to future employers

---

## 10. Evolution Path (Optional Extensions)

### 1: International Expansion
- New stakeholder: Regulatory Affairs (frequency allocation in EU vs US)
- New requirement: Localization for Spanish-speaking farmers
- New domain focus: OMD (managing deployments across regions)

### 2: Scale Challenge
- Customer: Large greenhouse operation (500 nodes)
- New concerns: Network capacity planning, centralized vs distributed architecture
- New viewpoint: Business (cost per hectare vs flat fee)

### 3: Post-Deployment
- Customer support tickets drive firmware updates
- OTA update strategy
- Field failure analysis

---

## Appendix: Stakeholder Profiles (Detailed)

### Eng. Samuel - Senior IoT Architect
- **Background**: Electronics Engineer, IoT Expert with extensive experience in embedded systems and wireless networks
- **Personality**: Mentoring but rigorous, values learning over perfection
- **Pet peeves**: Hand-waving explanations, copy-paste without understanding
- **Catch phrase**: "Show me the numbers" / "Which domain does this belong to?"

**What he looks for in your DDRs**:
- Correct use of ISO/IEC 30141 terminology
- Quantitative justification (not "seems faster")
- Explicit acknowledgment of tradeoffs
- Evidence of first-principles thinking

---

### Gustavo - Product Owner
- **Background**: MBA, former farmer-turned-entrepreneur
- **Personality**: Optimistic, customer-obsessed, pragmatic about tradeoffs
- **Pet peeves**: Over-engineering, missed deadlines, vague estimates
- **Catch phrase**: "Will farmers pay for this feature?"

**What he cares about**:
- Cost (BOM, development time)
- Customer-facing features
- Time to market
- Competitive differentiation

---

### Edwin - Field Operations Lead
- **Background**: Agricultural engineer, manages pilot deployments
- **Personality**: Detail-oriented, risk-averse, field-tested wisdom
- **Pet peeves**: Solutions that work "in the lab" but fail in the field
- **Catch phrase**: "How do I troubleshoot this at 6 AM in a muddy field?"

**What she cares about**:
- Deployment simplicity
- Failure modes and diagnostics
- Environmental robustness
- Maintenance burden

---

### Sebastian - Security Lead
- **Background**: Cybersecurity, previously at industrial control systems company
- **Personality**: Skeptical, threat-model driven, pragmatic about risk
- **Pet peeves**: "Security through obscurity", unpatched vulnerabilities
- **Catch phrase**: "What's the attack surface?"

**What he cares about**:
- Data confidentiality and integrity
- Device authentication
- Compliance (GDPR, agricultural data regulations)
- Update mechanisms for vulnerability patches

---

### Daniela - Pilot Customer (Vegetable Farm)
- **Background**: Third-generation farmer, 20-hectare organic vegetable operation
- **Personality**: Practical, tech-curious but not tech-savvy, budget-conscious
- **Pet peeves**: Complicated setup, data without actionable insights
- **Catch phrase**: "Will this actually help me grow better tomatoes?"

**What she cares about**:
- Ease of installation (no IT background)
- Clear, actionable information
- Return on investment
- Reliability (can't babysit technology during harvest season)

---

**End of Project Briefing**

**Next Steps**: Review [README.md](README.md) for how this scenario integrates with the 8-lab curriculum.
