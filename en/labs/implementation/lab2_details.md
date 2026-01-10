# Lab 2 — 6LoWPAN + Routing & Resilience

> **Main Lab Guide:** [Lab 2: 6LoWPAN Mesh Networking](../lab2.md)
> **ISO Domains:** RAID (Resource Access & Interchange), SCD (Sensing & Controlling Domain)
> **GreenField Context:** Building self-healing mesh network for "Far Field" coverage

## Objectives
- Enumerate and classify IPv6 addresses (link-local, mesh-local, ML-EID).
- Observe 6LoWPAN fragmentation.
- Evaluate re-attach and role changes (leader, routers, children).

## Context
This implementation guide provides step-by-step technical instructions for 6LoWPAN networking and Thread routing. It complements the [main lab guide](../lab2.md) which covers the "Tractor Test" scenario and stakeholder context.

## Project Setup

### 1. Create Project from ESP-IDF Example

Use the ESP-IDF extension in VS Code:
1. Press `Ctrl+Shift+P` to open the command palette.
2. Search for and run `ESP-IDF: Show Examples` selecting your ESP-IDF version.
3. Select `openthread/ot_cli` (OpenThread CLI Example).
4. Select the folder to create the project.

### 2. Explore the OpenThread CLI Example Code

The `openthread/ot_cli` example includes code for basic Thread CLI. Examine the main files in the created project directory:

- `main/esp_ot_cli.c`: Entry point for the CLI example
- OpenThread components for Thread network handling

### 3. Build and Flash the Project

The example uses default configurations suitable for Thread/6LoWPAN. No changes to sdkconfig are required for this basic lab.

Use the ESP-IDF toolbar in VS Code:
1. Click **ESP-IDF: Set Target** and select `esp32c6`.
2. Click **ESP-IDF: Build Project**.
3. Connect the ESP32-C6 and click **ESP-IDF: Flash Device**.
4. Click **ESP-IDF: Monitor Device**.

### 4. Explore Thread/6LoWPAN CLI Commands

Once in the device console, use the example's CLI commands (all commands are documented in `help`):

```bash
# View full help
help

# View interface status
ifconfig

# View assigned IPv6 addresses
ipaddr

# View multicast addresses
ipmaddr

# View router table
router table

# View neighbor table
neighbor table

# View routes
routes
```

### 5. Basic Thread Network Formation

**Configure Device A (Leader):**
```bash
# Create new network dataset
dataset init new

# Configure channel and PAN ID
dataset channel 15
dataset panid 0x1234

# Configure master key
dataset masterkey 00112233445566778899aabbccddeeff

# Activate dataset
dataset commit active

# Start interface and Thread
ifconfig up
thread start
```

**Configure Device B (Router/Child):**
```bash
# Get dataset from leader (on device A)
# dataset active -x

# Copy the hex dataset to device B
dataset set active <leader_hex_dataset>

# Start interface and Thread
ifconfig up
thread start
```

**Verify network formation:**
- Both devices should join the Thread network
- Use `state` to see roles (leader, router, child)
- Use `ipaddr` to see assigned IPv6 addresses

### 6. IPv6 Address Analysis in 6LoWPAN

**Types of addresses to observe:**

1. **Link-local**: Prefix `fe80::/10`, used for local communication
2. **Mesh-local**: Prefix derived from dataset (e.g., `fd11:22:33::/64`), used within the mesh
3. **ML-EID (Mesh-Local EID)**: Unique device address in the mesh

**Commands for analysis:**
```bash
# View all addresses
ipaddr

# View multicast addresses (including All-Thread-Nodes)
ipmaddr

# View dataset details (to understand prefixes)
dataset active
```

**Analysis:**
- Document each address type and its purpose
- Observe how addresses change when joining different networks
- Compare addresses between devices on the same network

### 7. 6LoWPAN Fragmentation Observation

**Force fragmentation with large pings:**
```bash
# Normal ping (no fragmentation)
ping fd11:22:33:0:0:0:0:1

# Ping with large payload (will force 6LoWPAN fragmentation)
ping fd11:22:33:0:0:0:0:1 size 200

# Even larger ping
ping fd11:22:33:0:0:0:0:1 size 500
```

**Observe in logs:**
- Look for "Fragment" or "Reassembly" messages in the logs
- Note the effective 6LoWPAN MTU (~1280 bytes IPv6, but fragmented at lower layers)
- Measure additional latency due to fragmentation

**Fragmentation analysis:**
- Compare response times between small and large pings
- Document the maximum size without fragmentation
- Observe behavior with multiple hops in the mesh

### 8. Resilience and Re-attach Evaluation

**Simulate leader failure:**
1. Identify which device is the leader (`state` command)
2. Turn off the leader device (disconnect USB)
3. Observe on the remaining device:
   ```bash
   # View state change
   state

   # View re-attach logs
   # (automatic logs will show MLE messages)
   ```

**Measure convergence times:**
- Record timestamp when leader is turned off
- Record when new leader is elected (`state` changes)
- Calculate convergence time

**Additional resilience tests:**
```bash
# View MLE (Mesh Link Establishment) messages
mle

# Force role change (if router)
# (restart device and observe re-attach)

# Test with 3+ devices to see mesh routing
router table
neighbor table
```

**Resilience analysis:**
- Document the sequence of events during re-attach
- Measure convergence times for different network sizes
- Observe how IPv6 addresses are maintained during changes

### 9. Thread Routing Analysis

**Commands for routing analysis:**
```bash
# View router table
router table

# View neighbor table
neighbor table

# View active routes
routes

# View network topology
neighbor table
```

**Routing experiments:**
1. **Direct routing:** Ping between directly connected devices
2. **Mesh routing:** Ping between devices with intermediaries
3. **Routing with failure:** Repeat after simulating failure

**Analysis:**
- Document how the mesh topology is built
- Observe changes in routing tables during resilience tests
- Compare efficiency of direct routing vs mesh

## Deliverables
- Table of IPv6 addresses classified by type
- Fragmentation logs with overhead analysis
- Convergence time measurements for re-attach
- Thread network topology diagrams with roles
- Comparative performance analysis with/without fragmentation
