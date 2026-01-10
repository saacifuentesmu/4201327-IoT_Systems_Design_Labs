# Lab 3 — Thread/CoAP Basic

> **Main Lab Guide:** [Lab 3: Efficient Data Transport](../lab3.md)
> **ISO Domains:** ASD (Application & Service Domain), UD (User Domain)
> **GreenField Context:** Solving Emma's battery drain problem with CoAP/CBOR efficiency

## Objectives
- Implement `/light` (GET/PUT) and `/sensor` (GET mock JSON) endpoints over CoAP on an existing Thread network.
- Understand CoAP vs HTTP (overhead, methods, response codes).
- Test basic CoAP communication using Thread CLI.

## Context
This implementation guide provides step-by-step technical instructions for CoAP server implementation. It complements the [main lab guide](../lab3.md) which covers the energy efficiency rationale and CBOR compression theory.

## Project Setup

### 1. Create Project from ESP-IDF Example
```bash
idf.py create-project-from-example "$IDF_PATH/examples/openthread/ot_cli" lab03
cd lab03
```

### 2. Add CoAP Code Incrementally

**Modify `main/main.c`** (add call to CoAP server):
```c
// Add at the end of app_main(), after esp_openthread_cli_init():
ESP_LOGI(TAG, "OpenThread initialized with CLI");

// Start CoAP server
start_coap_server();
```

**Add forward declaration** at the beginning of the file:
```c
static const char *TAG = "iot_lab_base";

// Forward declaration
void start_coap_server(void);
```

**Create `main/coap_demo.c`**:

**Step 1: Add includes and basic CoAP setup**
```c
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <sys/select.h>
#include <errno.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "coap3/coap.h"

static const char *TAG = "coap_demo";
#define COAP_PORT 5683
static bool light_on = false;
static uint32_t sensor_counter = 0;

void start_coap_server(void)
{
    xTaskCreate(coap_server_task, "coap_server", 4096, NULL, 5, NULL);
}
```

**Step 2: Add socket initialization**
```c
static void coap_server_task(void *pvParameters)
{
    coap_context_t *ctx = NULL;
    coap_address_t dst;
    coap_resource_t *light_resource = NULL;
    coap_resource_t *sensor_resource = NULL;
    fd_set readfds;
    struct timeval tv;
    int result;
    coap_log_t log_level = COAP_LOG_WARN;

    coap_set_log_level(log_level);
    coap_set_log_handler(NULL);

    coap_address_init(&dst);
    dst.addr.sin6.sin6_family = AF_INET6;
    dst.addr.sin6.sin6_port = htons(COAP_PORT);
    dst.addr.sin6.sin6_addr = in6addr_any;

    ctx = coap_new_context(NULL);
    if (!ctx) {
        ESP_LOGE(TAG, "Failed to create CoAP context");
        return;
    }

    coap_new_endpoint(ctx, &dst, COAP_PROTO_UDP);

    // Resources will be added in subsequent steps

    ESP_LOGI(TAG, "CoAP server started on port %d", COAP_PORT);

    while (1) {
        FD_ZERO(&readfds);
        FD_SET(coap_context_get_coap_fd(ctx), &readfds);
        tv.tv_sec = 1;
        tv.tv_usec = 0;

        result = select(FD_SETSIZE, &readfds, 0, 0, &tv);
        if (result > 0) {
            if (FD_ISSET(coap_context_get_coap_fd(ctx), &readfds)) {
                coap_io_process(ctx, COAP_IO_WAIT);
            }
        } else if (result < 0) {
            break;
        }
    }

finish:
    coap_free_context(ctx);
    coap_cleanup();
    vTaskDelete(NULL);
}
```

**Step 3: Add /light handler**
```c
static void handle_light(coap_context_t *ctx, coap_resource_t *resource,
                          coap_session_t *session, coap_pdu_t *request,
                          coap_binary_t *token, coap_string_t *query,
                          coap_pdu_t *response)
{
    const char *response_data;
    size_t response_data_len;

    switch (request->code) {
    case COAP_REQUEST_GET:
        response->code = COAP_RESPONSE_CODE_CONTENT;
        response_data = light_on ? "1" : "0";
        response_data_len = strlen(response_data);
        coap_add_data_blocked_response(resource, session, request, response,
                                        token, COAP_MEDIATYPE_TEXT_PLAIN, 0,
                                        response_data_len,
                                        (const uint8_t *)response_data);
        break;
    case COAP_REQUEST_PUT:
        if (request->data && request->data->length == 1 &&
            (request->data->s[0] == '0' || request->data->s[0] == '1')) {
            light_on = (request->data->s[0] == '1');
            response->code = COAP_RESPONSE_CODE_CHANGED;
        } else {
            response->code = COAP_RESPONSE_CODE_BAD_REQUEST;
        }
        break;
    default:
        response->code = COAP_RESPONSE_CODE_METHOD_NOT_ALLOWED;
        break;
    }
}
```

Add in `coap_server_task`, replacing the comment `// Resources will be added in subsequent steps`:
```c
light_resource = coap_resource_init(coap_make_str_const("light"), 0);
if (!light_resource) {
    ESP_LOGE(TAG, "Failed to create light resource");
    goto finish;
}
coap_register_handler(light_resource, COAP_REQUEST_GET, handle_light);
coap_register_handler(light_resource, COAP_REQUEST_PUT, handle_light);
coap_add_resource(ctx, light_resource);
```

**Step 4: Add /sensor handler**
```c
static void handle_sensor(coap_context_t *ctx, coap_resource_t *resource,
                           coap_session_t *session, coap_pdu_t *request,
                           coap_binary_t *token, coap_string_t *query,
                           coap_pdu_t *response)
{
    char payload[32];
    size_t len;

    if (request->code != COAP_REQUEST_GET) {
        response->code = COAP_RESPONSE_CODE_METHOD_NOT_ALLOWED;
        return;
    }

    sensor_counter++;
    len = snprintf(payload, sizeof(payload), "{\"val\":%u}", sensor_counter);
    response->code = COAP_RESPONSE_CODE_CONTENT;
    coap_add_data_blocked_response(resource, session, request, response,
                                    token, COAP_MEDIATYPE_APPLICATION_JSON, 0,
                                    len, (const uint8_t *)payload);
}
```

Add in `coap_server_task`, after the light_resource code:
```c
sensor_resource = coap_resource_init(coap_make_str_const("sensor"), 0);
if (!sensor_resource) {
    ESP_LOGE(TAG, "Failed to create sensor resource");
    goto finish;
}
coap_register_handler(sensor_resource, COAP_REQUEST_GET, handle_sensor);
coap_add_resource(ctx, sensor_resource);
```

**Modify `main/CMakeLists.txt`** to include CoAP:
```cmake
idf_component_register(SRCS "main.c" "coap_demo.c"
                        INCLUDE_DIRS "."
                        REQUIRES openthread libcoap esp_openthread_cli)
```

### 3. Configure Settings

**Create/update `sdkconfig`** with required configurations:
```bash
# OpenThread Configuration
CONFIG_OPENTHREAD_ENABLED=y
CONFIG_OPENTHREAD_CLI=y
CONFIG_OPENTHREAD_FTD=y
CONFIG_OPENTHREAD_JOINER=y

# Network Configuration
CONFIG_LWIP_IPV6=y

# CoAP
CONFIG_COAP_ENABLED=y

# ESP32-C6 specific
CONFIG_IDF_TARGET="esp32c6"
```

**Build and flash:**
```bash
idf.py set-target esp32c6
idf.py build
idf.py flash
idf.py monitor
```

### 4. Test CoAP Using CLI

For this lab, CoAP tests are performed directly from the Thread CLI on a second ESP32 node. Connect a second device and join the Thread network of the first node.

**On the second node (client):**
```bash
# Get dataset from leader (on the first device)
# dataset active -x

# Copy the hex dataset to the second device
dataset set active <leader_hex_dataset>
ifconfig up
thread start

# Once joined, test CoAP from CLI
coap get [Server IPv6] /sensor
coap put [Server IPv6] /light 1
```

## Deliverables
- CLI captures showing Thread network formation (from Lab 2)
- CoAP server logs with GET/PUT requests to `/light` and `/sensor`
- CoAP vs HTTP comparison (overhead, methods, response codes)
- Documentation of implemented endpoints and their functionality
