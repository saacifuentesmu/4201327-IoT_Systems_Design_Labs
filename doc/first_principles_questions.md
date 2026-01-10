# First Principles: The "Why?" Questions

> Don't just use technology—understand the physics and math underneath.

---

## Lab 1: IEEE 802.15.4 Fundamentals

### Q1: Why does 802.15.4 use O-QPSK modulation?
**Short Answer:** Better noise immunity than simpler schemes (FSK) at similar complexity.

**Deep Dive:** O-QPSK (Offset Quadrature Phase Shift Keying) minimizes amplitude variations during symbol transitions, reducing power amplifier requirements (critical for battery devices). It provides ~8 dB better link margin than FSK at similar data rates.

**Trade-off:** More complex demodulator vs. better range/power efficiency.

---

### Q2: Why 16 channels in 2.4 GHz band?
**Short Answer:** Balance between frequency diversity and regulatory compliance.

**Deep Dive:**
- 2400-2483.5 MHz ISM band = 83.5 MHz
- Channel spacing: 5 MHz (minimizes adjacent channel interference)
- 83.5 MHz / 5 MHz ≈ 16 channels
- Channels 11-26 selected to coexist with WiFi (channels 1, 6, 11)

**Design Principle:** Spectrum efficiency under regulatory constraints.

---

### Q3: Why is CCA (Clear Channel Assessment) necessary?
**Short Answer:** Collision avoidance in shared spectrum.

**Deep Dive:**
- 2.4 GHz is unlicensed (WiFi, Bluetooth, Zigbee, microwaves all share it)
- Without CCA: hidden terminal problem → packet collisions → wasted energy
- CCA implements CSMA/CA (Carrier Sense Multiple Access with Collision Avoidance)
- Energy detection threshold: typically -75 to -85 dBm

**Physical Principle:** Listen before transmit minimizes interference.

---

## Lab 2: 6LoWPAN + Thread Routing

### Q4: Why compress IPv6 headers in 6LoWPAN?
**Short Answer:** 802.15.4 MTU is only 127 bytes; standard IPv6 header is 40 bytes.

**Math:**
- IPv6 header: 40 bytes
- UDP header: 8 bytes
- 802.15.4 frame: 127 bytes max
- Payload without compression: 127 - 40 - 8 = 79 bytes (only 62% efficiency!)
- With 6LoWPAN IPHC compression: ~2-6 bytes for IPv6 header
- Compressed payload: 127 - 6 - 8 = 113 bytes (89% efficiency)

**Gain:** +43% usable payload per packet = fewer transmissions = lower power.

---

### Q5: Why mesh topology instead of star?
**Short Answer:** Range extension + reliability without infrastructure.

**Network Theory:**
- Star: All nodes must reach gateway directly (limited by TX power × path loss)
- Mesh: Multi-hop routing extends effective range (3 hops @ 30m each = 90m coverage)
- Reliability: If one parent fails, children can re-attach to different parent (self-healing)

**Trade-off:** Increased latency (each hop adds ~10-30ms) vs. extended coverage.

---

## Lab 3: CoAP Protocol

### Q6: Why does CoAP use UDP instead of TCP?
**Short Answer:** UDP avoids TCP overhead (connection setup, window management, retransmissions).

**Overhead Analysis:**
```
TCP Connection Setup:
SYN → SYN-ACK → ACK (3-way handshake)
= 3 packets × (20 byte TCP header + 40 byte IPv6 header)
= 180 bytes just to establish connection!

UDP:
Send data immediately, no connection setup
= 8 byte UDP header

Savings: 180 - 8 = 172 bytes = 95% reduction in overhead
```

**CoAP's Solution:**
- UDP for low overhead
- Confirmable (CON) messages for reliability when needed
- Application-layer retransmission with exponential backoff

**Design Principle:** Simplicity at lower layer, flexibility at higher layer.

---

### Q7: Why 4-byte CoAP header vs ~200-byte HTTP header?
**Short Answer:** Binary encoding vs. text encoding.

**Comparison:**
```
HTTP GET:
GET /temperature HTTP/1.1
Host: sensor.local
User-Agent: curl/7.68.0
Accept: */*

= ~120 bytes (text)

CoAP GET:
Ver(2b) Type(2b) TKL(4b) Code(8b) MsgID(16b) Token(32b) Options(variable)
= 4-10 bytes (binary)

Compression ratio: 120/10 = 12× smaller
```

**Principle:** Binary protocols minimize wire representation at cost of human readability.

---

## Lab 4: Power Management

### Q8: Why does sleep mode save so much power?
**Short Answer:** Most power consumed by radio (70-100 mA TX); sleep disables radio (< 5 mA).

**Physics:**
```
Power = Voltage × Current
Energy = Power × Time

Active mode:
P = 3.3V × 80mA = 264 mW
Energy per hour: 264mW × 3600s = 950 J

Sleep mode:
P = 3.3V × 2mA = 6.6 mW
Energy per hour: 6.6mW × 3600s = 24 J

Ratio: 950 / 24 = 40× less energy in sleep!
```

**Implication:** 10% duty cycle = ~90% energy savings.

---

### Q9: Why is light sleep (15 mA) more expensive than deep sleep (2 mA)?
**Short Answer:** Light sleep keeps RAM powered and listens for radio wakeup; deep sleep shuts down everything except RTC.

**Component Breakdown:**
- RAM retention: ~8 mA
- Radio RX (periodic listening): ~5 mA
- CPU idle: ~2 mA
- **Light sleep total:** ~15 mA

- RTC (wake-on-timer): ~2 mA only
- **Deep sleep total:** ~2 mA

**Trade-off:** Light sleep wakes faster (~3ms) vs deep sleep (~100ms boot time).

---

## Lab 5: CoAP Observe (Pub/Sub)

### Q10: Why is Observe more efficient than polling?
**Short Answer:** Server only sends when data changes vs. client polling every N seconds regardless.

**Traffic Analysis:**
```
Polling (every 2 seconds, temperature stable for 10 minutes):
Requests: 600s / 2s = 300 requests
Traffic: 300 × (30 byte request + 50 byte response) = 24,000 bytes

Observe (1 change per 10 minutes):
Registration: 1 request (30 bytes)
Notifications: 1 change (50 bytes)
Traffic: 30 + 50 = 80 bytes

Efficiency gain: 24,000 / 80 = 300× reduction!
```

**Principle:** Event-driven > time-driven when events are sparse.

---

## Lab 6: Cryptography

### Q11: Why RSA-2048 instead of RSA-1024?
**Short Answer:** RSA-1024 can be broken by nation-states (estimated < $100M compute); RSA-2048 is still secure.

**Security Math:**
- RSA security based on difficulty of factoring N = p × q (two large primes)
- RSA-1024: ~80-bit security (2^80 operations to break)
- RSA-2048: ~112-bit security (2^112 operations)
- Difference: 2^112 / 2^80 = 2^32 = 4 billion times harder

**NIST Recommendation:** RSA-2048 minimum for systems needing security beyond 2030.

**Trade-off:** RSA-2048 signature verification takes ~2-3 seconds on ESP32 (but done once per OTA update, acceptable).

---

### Q12: Why sign firmware instead of just encrypting it?
**Short Answer:** Signatures prove authenticity (who created it); encryption proves confidentiality (who can read it).

**Threat Model:**
- **Without signature:** Attacker replaces firmware with malicious version
- **With signature:** Bootloader verifies signature; rejects tampered firmware
- **Encryption alone:** Attacker can't read firmware but can still replace it

**Principle:**
- Signatures = integrity + authenticity
- Encryption = confidentiality
- Both are needed for different threats

---

## Lab 7: Caching & Rate Limiting

### Q13: Why does caching work for IoT sensor data?
**Short Answer:** Physical processes (temperature, humidity) change slowly relative to query rate.

**Physics:**
- Room temperature thermal time constant: ~10-30 minutes
- Dashboard polling rate: 1-2 seconds
- Staleness ratio: 600s / 2s = 300 queries per actual change

**Cache Strategy:**
```
TTL = 5 seconds (sensor read every 5s instead of every request)
If temperature changes < 0.5°C, cached value is "good enough"

Cache hit rate = (queries - sensor_reads) / queries
If 100 queries over 5 seconds:
Hit rate = (100 - 1) / 100 = 99%

Result: 99× fewer I2C reads = lower power + faster response
```

---

### Q14: Why implement rate limiting?
**Short Answer:** Protect device from resource exhaustion (DoS attack or buggy client).

**Token Bucket Algorithm:**
```
Capacity: 10 tokens (max burst)
Refill rate: 1 token/second (sustained rate)

Normal client (1 req/2sec): Never blocked
Malicious client (100 req/sec):
  - First 10 requests succeed (burst)
  - Remaining 90 blocked
  - Device stays responsive
```

**Principle:** Fairness under overload.

---

## Application to Your Labs

**For each lab, ask:**
1. **What?** What technology are we using?
2. **How?** How do we implement it?
3. **Why?** Why was it designed this way? (← This is first principles thinking!)

**Document answers in your DDR under "First Principles Reflections"**

---

## Further Reading (Optional)

- **Lab 1:** "IEEE 802.15.4 Standard" (free PDF from IEEE)
- **Lab 2:** RFC 6282 (6LoWPAN compression)
- **Lab 3:** RFC 7252 (CoAP protocol)
- **Lab 6:** "Introduction to Modern Cryptography" by Katz & Lindell
- **Shannon's Theorem:** Information theory limits (Lab 1-2 context)
