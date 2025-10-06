# Lab 3 — Thread/CoAP Basic

## Objetivos
- Implementar endpoints `/light` (GET/PUT) y `/sensor` (GET mock JSON) sobre CoAP en red Thread existente.
- Comprender CoAP vs HTTP (overhead, métodos, códigos respuesta).
- Probar comunicación CoAP básica usando CLI Thread.

## Contexto
Construyendo sobre las redes Thread establecidas en Lab 2, este laboratorio introduce CoAP como protocolo de aplicación ligero para IoT, implementando servicios RESTful sobre IPv6/6LoWPAN y comparando con HTTP tradicional.

## Setup del Proyecto

### 1. Crear proyecto desde ejemplo ESP-IDF
```bash
idf.py create-project-from-example "$IDF_PATH/examples/openthread/ot_cli" lab03
cd lab03
```

### 2. Añadir código CoAP incrementalmente

**Modificar `main/main.c`** (añadir llamada al servidor CoAP):
```c
// Añadir al final de app_main(), después de esp_openthread_cli_init():
ESP_LOGI(TAG, "OpenThread initialized with CLI");

// Start CoAP server
start_coap_server();
```

**Añadir declaración forward** al inicio del archivo:
```c
static const char *TAG = "iot_lab_base";

// Forward declaration
void start_coap_server(void);
```

**Crear `main/coap_demo.c`**:

**Paso 1: Añadir includes y setup básico de CoAP**
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

**Paso 2: Añadir inicialización de socket**
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

**Paso 3: Añadir handler /light**
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

Añadir en `coap_server_task`, reemplazando el comentario `// Resources will be added in subsequent steps`:
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

**Paso 4: Añadir handler /sensor**
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

Añadir en `coap_server_task`, después del código del light_resource:
```c
sensor_resource = coap_resource_init(coap_make_str_const("sensor"), 0);
if (!sensor_resource) {
    ESP_LOGE(TAG, "Failed to create sensor resource");
    goto finish;
}
coap_register_handler(sensor_resource, COAP_REQUEST_GET, handle_sensor);
coap_add_resource(ctx, sensor_resource);
```

**Modificar `main/CMakeLists.txt`** para incluir CoAP:
```cmake
idf_component_register(SRCS "main.c" "coap_demo.c"
                        INCLUDE_DIRS "."
                        REQUIRES openthread libcoap esp_openthread_cli)
```

### 3. Configurar settings

**Crear/actualizar `sdkconfig`** con configuraciones necesarias:
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

**Build y flash:**
```bash
idf.py set-target esp32c6
idf.py build
idf.py flash
idf.py monitor
```

### 4. Probar CoAP usando CLI

Para este laboratorio, las pruebas CoAP se realizan directamente desde la CLI de Thread en un segundo nodo ESP32. Conecta un segundo dispositivo y únete a la red Thread del primer nodo.

**En el segundo nodo (cliente):**
```bash
# Obtener dataset del líder (en el primer dispositivo)
# dataset active -x

# Copiar el dataset hexadecimal al segundo dispositivo
dataset set active <dataset_hex_del_líder>
ifconfig up
thread start

# Una vez unido, probar CoAP desde CLI
coap get [IPv6 del servidor] /sensor
coap put [IPv6 del servidor] /light 1
```

## Entregables
- Capturas de CLI mostrando formación de red Thread (de Lab 2)
- Logs de servidor CoAP con requests GET/PUT a `/light` y `/sensor`
- Comparación CoAP vs HTTP (overhead, métodos, códigos de respuesta)
- Documentación de endpoints implementados y su funcionalidad