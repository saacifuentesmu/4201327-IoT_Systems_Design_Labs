# SOP-05: Border Router Deployment

> **Main Lab Guide:** [Lab 5: Border Router](../lab5.md)
> **ISO Domains:** RAID (Resource Access & Interchange), SCD (Sensing & Controlling)
> **GreenField Context:** Enabling remote access for Maria (Ops) via Internet gateway

## Objectives
Deploy an **Edge Gateway** to bridge the IEEE 802.15.4 Mesh to the IPv6 Internet. Validate the **Construction Viewpoint** (Gateway Pattern).

## Setup
* **Hardware:**
    * 1x ESP32-C6 (Flashed as RCP - Radio Co-Processor).
    * 1x Laptop/Raspberry Pi (Host running Docker).
* **Software:** `esp-idf`, `docker`.

## Procedure

### 3.1 Flash the Radio Co-Processor (RCP)
The RCP does not run application logic. It acts as a "dumb modem" for the computer.
1.  Open project: `examples/openthread/ot_rcp`
2.  Build & Flash to the ESP32-C6 connected to USB.
    ```bash
    idf.py set-target esp32c6
    idf.py build flash
    ```
3.  **Note the Serial Port:** (e.g., `/dev/ttyUSB0` or `COM3`).

### 3.2 Run the OTBR Container
We use the official OpenThread Docker image.
* **Command (Linux/Mac):**
    ```bash
    docker run --sysctl "net.ipv6.conf.all.disable_ipv6=0" \
        --sysctl "net.ipv4.conf.all.forwarding=1" \
        --sysctl "net.ipv6.conf.all.forwarding=1" \
        -p 8080:80 --dns=127.0.0.1 -it \
        --volume /dev/ttyUSB0:/dev/ttyUSB0 \
        --privileged openthread/otbr-sel-ci:latest \
        --radio-url spinel+hdlc+uart:///dev/ttyUSB0
    ```
* **Verify:** Open a web browser to `http://localhost:8080`. You should see the OpenThread GUI.

### 3.3 Form the Network (Global Prefix)
In the Web GUI:
1.  **Form** a new network.
2.  **Prefix:** Ensure you obtain a Global IPv6 Prefix (e.g., `fd11:22::/64`) so nodes can routable.

### 3.4 The "Ping Google" Test
1.  Go to a **Sensor Node** (from Lab 3/4).
2.  Check its IP addresses: `ipaddr`. You should see a new global address (matching the OTBR prefix).
3.  Ping an external server (Google DNS IPv6):
    ```bash
    > ping 2001:4860:4860::8888
    ```
4.  **Success Criteria:** If you get a reply, your battery-powered sensor is talking to the Internet.

## Verification (DDR Data)
* **Topology:** Take a screenshot of the OTBR Web Topology view.
* **Latency:** Measure ping time to the OTBR (Local) vs. Google (Internet). Record the "Cloud Overhead."