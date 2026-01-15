# Networking Fundamentals & IoT Introduction

**GreenField Technologies - Onboarding Module**
**Phase**: Team Alignment
**Topic**: Networking Recap, IPv6, and IoT First Principles

---

## 1. Project Context: Why this module?

**From:** Eng. Samuel Cifuentes (Senior Architect)
**To:** New IoT Systems Engineering Team
**Subject:** Knowledge Alignment

Welcome to the team. Before we start building our precision agriculture mesh network, we need to ensure everyone is aligned on the fundamental technologies we use. We cannot afford architecture errors due to misunderstandings of basic networking principles.

**Objectives**:
1.  **Refresher**: Verify your understanding of core networking concepts (TCP/IP, Client-Server vs Peer-to-Peer).
2.  **IPv6 Deep Dive**: Our production system uses Thread (IPv6-based). You must understand why we don't use IPv4 and how to read an IPv6 address.
3.  **IoT Reality Check**: Understand the constraints that drive our decisions (Energy, Memory, Bandwidth).

---

## 2. Networking Recap - The Foundation

### What is the Internet?
At its core, the Internet is a global system of interconnected computer networks that use the standard Internet Protocol Suite (TCP/IP) to serve billions of users worldwide. It is a **network of networks**.

- **Protocol**: A set of rules that allow two or more entities to communicate. (e.g., "Speak English", "Wait for me to finish before you start").
- **Packet Switching**: Data is broken into small chunks (packets), sent independently, and reassembled at the destination. This is efficient and robust.

### The TCP/IP Model (Simplified)
For our IoT work, we care about these layers:
1.  **Application**: HTTP, CoAP, MQTT (What the user sees/uses).
2.  **Transport**: TCP (Reliable, heavy), UDP (Fast, fire-and-forget). *IoT often prefers UDP.*
3.  **Network**: IP (Addressing and Routing). *Getting packets from A to B across the world.*
4.  **Link/Physical**: Ethernet, WiFi, 802.15.4. *Getting packets from device to device.*

---

## 3. IPv4 vs IPv6 - The Critical Shift

Traditionally, the internet ran on **IPv4**.
- **Format**: `192.168.1.1` (32-bit addresses).
- **Limit**: ~4.3 billion addresses. We ran out years ago.
- **Workaround**: NAT (Network Address Translation). Your home router has ONE public IP, and all your devices hide behind it.

### Why IoT Needs IPv6
**IPv6** uses 128-bit addresses.
- **Format**: `2001:0db8:85a3:0000:0000:8a2e:0370:7334`.
- **Capacity**: $3.4 \times 10^{38}$ addresses. Enough to give every grain of sand on Earth its own IP.

**Key Advantages for GreenField:**
1.  **No NAT Needed**: Every sensor node has a globally unique public IP (conceptually). We can talk to them directly.
2.  **Auto-configuration (SLAAC)**: Devices generate their own addresses when they join the network. No DHCP server needed.
3.  **Efficiency**: Simplified header format for faster processing.

| Feature | IPv4 | IPv6 |
| :--- | :--- | :--- |
| Address Length | 32-bit | 128-bit |
| Example | `192.168.1.50` | `fe80::2f1a:3b4c:5d6e:7f8a` |
| Config | DHCP (Manual/Server) | SLAAC (Automatic) |
| Broadcast | Yes (Noisy) | No (Uses Multicast - Efficient) |

---

## 4. What is IoT?

**Internet of Things (IoT)** is the extension of internet connectivity into physical devices and everyday objects.

### Operational Technology (OT) vs Information Technology (IT)
- **IT (Laptops, Servers)**: Focus on high throughput, big data, human interaction. Power is usually unlimited (plugged in).
- **OT/IoT (Sensors, Actuators)**: Focus on reliability, real-time control, physical world interaction.

### The "Constraint" Triangle
In this course, you will realize that IoT engineering is the art of compromise:
1.  **Energy**: Batteries must last years. We sleep 99% of the time.
2.  **Memory**: We have KiloBytes, not GigaBytes. Code must be tiny.
3.  **Bandwidth**: We send bytes, not 4K video. Radio links are slow and unreliable.

---

## 5. Review Questions (Self-Check)

Answer the following **First Principles Questions** (add to your personal notes):
1.  Why can't we just give every sensor a static IPv4 address?
2.  What is the difference between a "Link-Local" address (starts with `fe80`) and a "Global" address?
3.  Why does the ESP32-C6 need to "sleep" instead of staying connected to WiFi all the time?
4.  If a device sends a UDP packet, does it know if the packet arrived? Why or why not?

---

### Navigation
[< Back to Setup](0_setup.md) | [Next: Project Scenario >](1_project_scenario.md)
