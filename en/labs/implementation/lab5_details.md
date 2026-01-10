# Lab 5 — Thread/CoAP Advanced & Border Router

> **Main Lab Guide:** [Lab 5: The Border Router](../lab5.md)
> **ISO Domains:** RAID (Resource Access & Interchange), Construction View
> **GreenField Context:** Enabling Emma to check her crops from her phone at the market

## Objectives
- Implement a Border Router (OTBR) with RCP ESP32-C6.
- Access Thread nodes from LAN (ping, CoAP).
- Add CoAP Observe to the `/sensor` resource.
- Network-based CoAP testing with Python client.
- (Optional) Introduce MQTT (local broker) as pub/sub comparison.

## Context
This implementation guide provides step-by-step technical instructions for Border Router deployment and CoAP Observe. It complements the [main lab guide](../lab5.md) which covers the Edge Gateway pattern and NAT64 translation theory.

## Project Setup

### 1. Create Separate RCP Project

For this lab, create a separate project for the Radio Co-Processor (RCP) that will connect to the Border Router running on the host:

Use the ESP-IDF extension in VS Code:
1. Press `Ctrl+Shift+P` to open the command palette.
2. Search for and run `ESP-IDF: Show Examples` selecting your ESP-IDF version.
3. Select `openthread/ot_rcp` (OpenThread RCP Example).
4. Select the folder to create the project (e.g., `lab05_rcp`).

### 2. Configure for RCP Mode (No Additional Code, RCP Doesn't Run Application)

The RCP (Radio Co-Processor) doesn't run application code; it only handles the Thread radio.
The CoAP server with observe runs on the CLI nodes (from previous Labs).

### 3. Configure Settings

**Configure sdkconfig for RCP:**
```bash
# The ot_rcp example already has base configurations
# Adjust if needed:
idf.py menuconfig
# Verify: CONFIG_OPENTHREAD_RCP=y
# Disable CLI and FTD since this is pure RCP
```

**Build and flash:**
```bash
idf.py set-target esp32c6
idf.py build
idf.py flash
# This device will act as RCP for OTBR running on the host
```

### 4. Configure OTBR and Test Connectivity

Follow the OTBR instructions to configure the Border Router on your host. Once configured, Thread nodes will be accessible from the LAN.

### 5. Test CoAP with Python Client (Network-based)

Now that the Border Router is active, you can use the Python client to access Thread nodes from your PC.

**Install dependencies on the host:**
```bash
pip install aiocoap
```

**Using the Python client:**
```bash
# Get sensor status
python tools/coap_client.py --host [Thread node IPv6] get /sensor

# Get light status
python tools/coap_client.py --host [Thread node IPv6] get /light

# Change light state (0=off, 1=on)
python tools/coap_client.py --host [Thread node IPv6] put /light 1
```

**Note:** Thread IPv6 addresses are now routable through the Border Router. Use `ipaddr` in the Thread CLI to get the addresses.

### 6. Add CoAP Observe to the `/sensor` Resource

**Modify `handle_sensor`** to support observe (on Thread nodes):

Add in `main/coap_demo.c`:
```c
// Add global variable for notifications
static coap_resource_t *sensor_resource = NULL;
static sensor_data_t last_notified_data = {0};

// Modify handle_sensor for observe
static void handle_sensor(coap_context_t *ctx, coap_resource_t *resource,
                          coap_session_t *session, coap_pdu_t *request,
                          coap_binary_t *token, coap_string_t *query,
                          coap_pdu_t *response)
{
    char payload[128];
    size_t len;

    if (request->code == COAP_REQUEST_GET) {
        // Read sensor
        read_sensor_mock(&current_sensor_data);

        len = snprintf(payload, sizeof(payload),
                       "{\"temp\":%.1f,\"hum\":%.1f,\"ts\":%u,\"seq\":%u}",
                       current_sensor_data.temperature,
                       current_sensor_data.humidity,
                       current_sensor_data.timestamp,
                       current_sensor_data.sequence);

        response->code = COAP_RESPONSE_CODE_CONTENT;
        coap_add_data_blocked_response(resource, session, request, response,
                                       token, COAP_MEDIATYPE_APPLICATION_JSON, 0,
                                       len, (const uint8_t *)payload);

        // For observe, remember last value
        last_notified_data = current_sensor_data;
    } else if (request->code == COAP_REQUEST_OBSERVE) {
        // Handle observe registration/deregistration
        coap_observe_add(resource, session, token);
        response->code = COAP_RESPONSE_CODE_CONTENT;
    } else {
        response->code = COAP_RESPONSE_CODE_METHOD_NOT_ALLOWED;
    }
}

// Function to send observe notifications
static void notify_sensor_observers(void)
{
    if (sensor_resource) {
        char payload[128];
        size_t len;

        // Only notify if data changed significantly
        if (abs(current_sensor_data.temperature - last_notified_data.temperature) > 0.5 ||
            abs(current_sensor_data.humidity - last_notified_data.humidity) > 2.0) {

            len = snprintf(payload, sizeof(payload),
                           "{\"temp\":%.1f,\"hum\":%.1f,\"ts\":%u,\"seq\":%u}",
                           current_sensor_data.temperature,
                           current_sensor_data.humidity,
                           current_sensor_data.timestamp,
                           current_sensor_data.sequence);

            coap_resource_notify_observers(sensor_resource, (const uint8_t *)payload, len);
            last_notified_data = current_sensor_data;
            ESP_LOGI(TAG, "Sensor observe notification sent");
        }
    }
}
```

**Modify sensor task** to notify observers:
```c
static void sensor_pm_task(void *pvParameters)
{
    while (1) {
        ESP_LOGI(TAG, "Sensor reading active");
        read_sensor_mock(&current_sensor_data);

        // Notify observers if there are changes
        notify_sensor_observers();

        ESP_LOGI(TAG, "Entering light sleep for 30s");
        esp_sleep_enable_timer_wakeup(30 * 1000000);
        esp_light_sleep_start();

        ESP_LOGI(TAG, "Woke up from sleep");
    }
}
```

### 7. CoAP Observe Tests with Network Client

**Test observe from PC:**
```bash
# Register for observe (will keep running)
python tools/coap_client.py --host [Thread node IPv6] observe /sensor

# In another terminal, trigger notifications by changing sensor (or waiting for natural changes)
# Notifications will appear automatically when the sensor changes
```

**Measure delivery metrics:**
- Notification success ratio
- Latency between sensor change and notification reception
- Observe overhead vs polling

## Deliverables
- Functional Border Router RCP with OTBR running
- LAN→Thread connectivity logs (ping, CoAP from PC)
- `/sensor` endpoint with CoAP observe support
- Observe demo with network client showing real-time notifications
- Delivery metrics (success ratio, notification latency)
