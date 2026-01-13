# SOP-01: Advanced MAC Layer Tuning

> **Main Lab Guide:** [Lab 1: RF Characterization](../lab1.md)
> **ISO Domains:** PED (Physical Entity Domain), SCD (Sensing & Controlling)
> **GreenField Context:** Optimizing radio behavior for high-density sensor environments

## Objectives
- Manipulate CSMA-CA parameters (CCA threshold).
- Observe behavior under "false busy" conditions.
- Visualize ARQ (Automatic Repeat Request) retries and failures.
- Analyze Promiscuous Mode traffic.

## Theory: The "Listen Before Talk" Logic

Before the ESP32-C6 transmits, it performs a **CCA (Clear Channel Assessment)**:
1.  It listens to the air for 128 microseconds.
2.  If Energy > **CCA Threshold**, it backs off (waits random time).
3.  If Energy < **CCA Threshold**, it transmits.

**The Danger:**
* **Threshold too High:** You talk over others (Collisions).
* **Threshold too Low:** You never talk (False Busy).

## Experiment A: The "Paranoid" Radio
*Goal: Force a "Channel Busy" failure without actual interference.*

1.  **Setup:**
    * **Node A (TX)**: Configure to talk to Node B.
    * **Node B (RX)**: Passive.

2.  **The Baseline:**
    * Run `ed` (Energy Detect). Note the noise floor (e.g., -92 dBm).
    * Send a packet: `ieee802154 tx -l 10` -> **Success**.

3.  **The Tweak:**
    * Set the CCA Threshold **BELOW** the noise floor.
    * If noise is -92, set threshold to -95.
    ```bash
    > ieee802154 set_cca_threshold -95
    ```

4.  **The Test:**
    * Try to transmit: `ieee802154 tx -l 10`
    * **Result:** The radio should report `ESP_ERR_IEEE802154_CCA_BUSY` (or similar failure).
    * *Why?* The radio thinks the background static is another device talking.

5.  **Fix:** Restore threshold to default (-75 dBm).

## Experiment B: The "Ghost" Packet (ACK Failure)
*Goal: Visualize the Automatic Retransmission (ARQ) mechanism.*

IEEE 802.15.4 hardware automatically retries if it doesn't hear an "ACK" (Acknowledgment) beep.

1.  **Setup:**
    * **Node A (TX)**: Ready to send.
    * **Node B (RX)**: **UNPLUG IT.** (simulate a dead battery).

2.  **The Test:**
    * On Node A, send a packet **requesting an ACK** (`-a` flag):
    ```bash
    > ieee802154 tx -a -l 10
    ```

3.  **The Observation (Timing):**
    * You will notice a small delay (milliseconds) before the CLI says "Fail".
    * **What happened?**
        1.  TX Packet (Wait 1ms) -> No ACK.
        2.  Random Backoff -> Retry 1.
        3.  Random Backoff -> Retry 2.
        4.  Random Backoff -> Retry 3 -> **Give Up**.

4.  **DDR Question:**
    * Why is "No ACK" different from "CCA Busy"? (One happens *before* TX, one happens *after*).

## Experiment C: Promiscuous Mode (The Matrix)
*Goal: See traffic that isn't yours.*

By default, the radio ignores packets that don't match its PANID or Address. **Promiscuous Mode** disables this filter.

1.  **Setup:**
    * **Node A:** Set `promiscuous` mode.
    ```bash
    > ieee802154 set_promiscuous 1
    > ieee802154 rx_on
    ```
2.  **Action:**
    * Wait 60 seconds.
    * You will likely see hex dumps scrolling.
    * **Analysis:** These are WiFi beacons (if overlapping) or other Zigbee/Thread devices in the building.

3.  **Decode Challenge:**
    * Look at the first byte of a captured frame.
    * If it is `0x41` or `0x61`, it's a Data Frame.
    * Can you find the **Sequence Number** (usually the 3rd byte)?

## Verification (DDR Data)
Update your DDR (Section: Lab 1 Extended):
* [ ] **CCA Threshold:** At what value did your radio stop transmitting?
* [ ] **Retries:** Did enabling ACKs make the transmission slower?