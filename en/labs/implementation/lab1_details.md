# Lab 1 — IEEE 802.15.4 Fundamentals (PHY/MAC/Sniffing)

> **Main Lab Guide:** [Lab 1: RF Characterization](../lab1.md)
> **ISO Domains:** PED (Physical Entity Domain), SCD (Sensing & Controlling Domain)
> **GreenField Context:** Validating ESP32-C6 radio for SoilSense agricultural deployment

## Objectives
- Understand 2.4 GHz channelization and 802.15.4 frames.
- Capture and classify Beacon, Data, Ack, MAC Command frames.
- Evaluate the impact of CCA threshold and backoff.

## Context
This implementation guide provides step-by-step technical instructions for the physical and link layers of IEEE 802.15.4. It complements the [main lab guide](../lab1.md) which covers first-principles theory and stakeholder context.

## Project Setup

### 1. Create Project from ESP-IDF Example

Use the ESP-IDF extension in VS Code:
1. Press `Ctrl+Shift+P` to open the command palette.
2. Search for and run `ESP-IDF: Show Examples` selecting your ESP-IDF version.
3. Select `ieee802154/ieee802154_cli` (IEEE802.15.4 Command Line Example).
4. Select the folder to create the project.

### 2. Explore the IEEE 802.15.4 Example Code

The `ieee802154/ieee802154_cli` example includes code for basic IEEE 802.15.4 communication. Examine the main files in the created project directory:

- `main/esp_ieee802154_cli.c`: Entry point for the CLI example
- `components/cmd_ieee802154/ieee802154_cmd.c`: CLI command implementation

### 3. Build and Flash the Project

The example uses default configurations suitable for IEEE 802.15.4, including physical parameters like frequency deviation according to the standard. No changes to sdkconfig are required.

Use the ESP-IDF toolbar in VS Code:
1. Click **ESP-IDF: Set Target** and select `esp32c6`.
2. Click **ESP-IDF: Build Project**.
3. Connect the ESP32-C6 and click **ESP-IDF: Flash Device**.
4. Click **ESP-IDF: Monitor Device**.

### 4. Explore IEEE 802.15.4 Parameters

Once in the device console, use the example's CLI commands (all commands are documented in `help`):

```bash
# View full help
help

# Set channel (11-26)
channel -s 15

# Get current channel
channel -g

# Set transmit power (-80 to -10 dBm)
txpower -s 10

# Get current power
txpower -g

# Set PAN ID
panid 0x1234

# Get PAN ID
panid -g

# Set short address
shortaddr 0x0001

# Get short address
shortaddr -g

# Set extended address
extaddr 0xaa 0xbb 0xcc 0xdd 0x00 0x11 0x22 0x33

# Get extended address
extaddr -g
```

### 5. Communication Between Devices

**Configure Device A (Coordinator):**
```bash
# Set PAN ID and addresses
panid 0x1234
shortaddr 0x0001
channel -s 15

# Enter receive mode
rx -r 1
```

**Configure Device B (Node):**
```bash
# Set same PAN ID, different address
panid 0x1234
shortaddr 0x0002
channel -s 15

# Transmit data to device A
tx 0x00 0x01 0x02 0x03  # Example data
```

**Verify communication:**
- Device A should receive the data transmitted by B
- Swap roles and test bidirectional transmission

### 6. Spectrum and Physical Layer Analysis

**Spectrum analysis with Spectrum Analyzer:**
- Observe 2.4GHz channel occupancy (channels 11-26, spaced every 5 MHz)
- Identify interference from WiFi, Bluetooth, microwaves
- Measure channel width (2 MHz), channel spacing (5 MHz), and RF bandwidth

**Physical layer analysis:**
- Verify the center frequency of each channel (e.g., channel 11: 2405 MHz)
- Observe O-QPSK modulation and DSSS spreading
- Measure signal strength and signal-to-noise ratio (SNR)

### 7. Experiments with CCA and Radio Parameters

**Adjust CCA threshold and mode:**
```bash
# View current CCA configuration
cca -g

# Set threshold (-60 dBm in the example)
cca -v -60

# Set CCA mode (1: ED, 2: carrier or ED, etc.)
cca -m 1
```

**Energy detection:**
```bash
# Scan energy for a specific duration
ed -d 2
```

**Detailed experiments:**

1. **Channel switching:** Test communication on different channels
   ```bash
   # Switch to channel 11, 15, 20, 26
   channel -s 11
   channel -s 15
   # etc.
   ```

2. **Transmit power:** Vary txpower (-80 to -10 dBm)
   ```bash
   txpower -s -10  # Maximum power
   txpower -s -80  # Minimum power
   ```

3. **CCA threshold:** Adjust sensitivity
    ```bash
    cca -v -70  # More sensitive
    cca -v -80  # Less sensitive
    ```

4. **CSMA-CA backoff:** Configure two devices transmitting data frequently on the same channel. Observe in the logs if there are retransmissions or delays due to backoff. Compare with a free channel.

**Measurements and analysis:**
- RSSI, LQI, PER, throughput
- Create a comparative performance table
- Document the impact of environmental interference
- Measure range vs. transmit power

## Deliverables
- CCA/channel comparison + interference analysis
- Performance measurement table (RSSI, LQI, PER, throughput)
- Spectrum analysis with interference identification
- Documentation of range vs. transmit power
