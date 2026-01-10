# Ethics & Privacy in IoT Systems

> "Just because we *can* collect data doesn't mean we *should*."

**For:** Week 11-12 Lecture (5-10 minutes)

---

## 1. IoT Privacy Concerns

### The Problem
IoT devices collect **continuous, granular data** about physical spaces and human behavior:
- Smart thermostats: When you're home/away
- Security cameras: Who visits, daily routines
- Wearables: Health metrics, location
- **Your course project:** Environmental sensors (could infer occupancy, activity)

### Key Privacy Risks

| Risk | Example | Consequence |
|------|---------|-------------|
| **Surveillance** | Camera feeds stored indefinitely | Loss of privacy, potential abuse |
| **Inference** | Temperature patterns reveal occupancy | Home invasion, stalking |
| **Data breach** | Poorly secured cloud database | Personal data leak |
| **Function creep** | "Just monitoring" → targeted ads → insurance pricing | Loss of autonomy |

---

## 2. Principles: Privacy by Design

### Minimize Data Collection
- **Collect only what you need:** Temperature for HVAC, not camera feed
- **Aggregate early:** Send "average occupancy" not raw motion data
- **Local processing:** Keep raw data on-device when possible

**Your Lab 4:** Sending temperature/humidity is reasonable; adding camera would require justification.

---

### User Control & Transparency
- **Informed consent:** Users know what data is collected
- **Access controls:** Users can view/delete their data
- **Opt-out options:** Disable features without breaking device

**Example:** Smart thermostat with physical "privacy mode" switch (disables occupancy detection).

---

### Security = Privacy
- **Encryption:** Data in transit (DTLS) and at rest
- **Authentication:** Only authorized users access data
- **Updates:** Patch vulnerabilities (your Lab 6 OTA!)

**Failure Case:** Mirai botnet (2016) - IoT cameras with default passwords became DDoS army.

---

## 3. Regulatory Landscape

### GDPR (Europe)
- **Right to access:** Users can request their data
- **Right to erasure:** "Right to be forgotten"
- **Data minimization:** Collect only necessary data
- **Penalties:** Up to 4% of global revenue

### Colombia (Ley 1581 de 2012)
- **Habeas data:** Right to know what data is collected
- **Prior consent:** Users must explicitly authorize data use
- **Purpose limitation:** Data used only for stated purpose

**Implication:** Your IoT designs must consider legal compliance, not just technical functionality.

---

## 4. Environmental Impact (E-Waste)

### The Scale
- **50 million tons** of e-waste generated globally per year
- IoT devices often have **short lifespans** (2-5 years) vs. 10+ year appliances
- **Low recycling rates:** ~17% of e-waste properly recycled

### Contributors
1. **Built-in obsolescence:** Cloud service shutdown = device becomes brick
2. **Non-repairable design:** Glued/soldered components
3. **Battery degradation:** Non-replaceable batteries
4. **Software abandonment:** No more updates after 2 years

---

### Sustainable Design Principles

#### 1. Design for Longevity
- **Modular hardware:** Replaceable batteries, upgradeable firmware
- **Local-first:** Device works without cloud (your Border Router approach!)
- **Open protocols:** Thread/CoAP are standards (vs proprietary)

#### 2. Right to Repair
- **Accessible documentation:** Schematics, repair manuals
- **Standard parts:** Use off-the-shelf components when possible
- **Update support:** Commit to firmware updates for 5+ years

#### 3. End-of-Life Planning
- **Recyclability:** Use materials that can be separated and recycled
- **Take-back programs:** Manufacturer accepts old devices for proper disposal
- **Repurposing:** Can device be reprogrammed for different use?

**Your ESP32-C6:** Fully reprogrammable! After this course, it can become a different project (not e-waste).

---

## 5. Case Studies

### ❌ Bad Example: Amazon Ring Doorbells
- **Issue:** Police partnerships gave law enforcement access to camera feeds without warrants
- **Privacy violation:** Users unaware their data shared with police
- **Lesson:** Third-party data access must be transparent

### ✅ Good Example: Apple HomeKit
- **Design:** All automation runs locally on HomePod/AppleTV (no cloud required)
- **Encryption:** End-to-end encrypted camera feeds
- **User control:** Users can disable features, delete data
- **Lesson:** Privacy-first architecture is possible (but requires design effort)

---

## 6. Ethical Questions for Your Project

Ask yourself when designing IoT systems:

### Data Collection
- [ ] Do I *need* this data to provide value, or is it "nice to have"?
- [ ] Can I achieve the same functionality with less data?
- [ ] How long do I need to store this data?

### User Agency
- [ ] Can users opt out without breaking core functionality?
- [ ] Do users understand what data is collected and why?
- [ ] Can users delete their data?

### Security
- [ ] What happens if this device is hacked?
- [ ] How do I handle security vulnerabilities discovered after deployment?
- [ ] Is the data encrypted in transit and at rest?

### Longevity
- [ ] Will this device work if my cloud service shuts down?
- [ ] Can users repair or upgrade this device?
- [ ] What happens to the device at end-of-life?

---

## 7. Discussion: Your AgroSentinel Project

**Scenario:** You deploy environmental sensors for coffee farmers.

**Ethical Considerations:**

1. **Data Ownership:** Who owns the sensor data?
   - Farmers? (They own the land)
   - Cooperative? (They funded deployment)
   - You? (You built the system)
   - **Answer:** Farmers should own their data (privacy by design)

2. **Data Access:** Should buyers (coffee exporters) access sensor data?
   - **Pro:** Verifiable environmental conditions (premium pricing)
   - **Con:** Leverage in price negotiations (power imbalance)
   - **Solution:** Farmers choose whether to share, and with whom

3. **Longevity:** What if cooperative can't afford maintenance after 3 years?
   - **Poor design:** Cloud-dependent system stops working
   - **Good design:** Local-first architecture (Border Router at cooperative)
   - **Best design:** Open-source firmware (community can maintain)

---

## 8. Commitment: Responsible IoT Engineering

As IoT engineers, commit to:

1. **Question data collection:** Always ask "Do we need this?"
2. **Design for privacy:** Encryption, local processing, user control
3. **Build for longevity:** Reprogrammable, repairable, open protocols
4. **Consider externalities:** E-waste, surveillance, power dynamics
5. **Stay informed:** Laws change, vulnerabilities emerge

**Remember:** Every design decision has ethical implications. Be intentional.

---

## Resources

- **Podcast:** "Your Undivided Attention" (on persuasive tech ethics)
- **Book:** "The Age of Surveillance Capitalism" by Shoshana Zuboff
- **Standard:** ISO/IEC 27701 (Privacy Information Management)
- **Colombia:** SIC (Superintendencia de Industria y Comercio) - Data protection guidelines

---

## Discussion Questions (for class)

1. Should IoT devices have a "privacy mode" by default (opt-in to features) or "full functionality" by default (opt-out)?
2. Who is responsible when an IoT device causes harm (e.g., hacked camera)? Manufacturer? User? Hacker?
3. Is it ethical to design devices with planned obsolescence if it enables lower cost for consumers?

**Time for reflection:** 5 minutes in groups, then class discussion.
