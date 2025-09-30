# Lab 7 — Observabilidad & Optimización

## Objetivos
- Recolectar métricas (latencia, pérdida, throughput notificaciones).
- Implementar caching y rate limiting en dashboard.
- (Opcional) Streaming (WebSocket/SSE) para actualizaciones push.
- Añadir token simple de acceso (hardcoded o .env).

## Contexto
Construyendo sobre conceptos de observabilidad, este laboratorio optimiza el rendimiento del sistema IoT mediante recolección de métricas, estrategias de caching y rate limiting para asegurar manejo de datos confiable y eficiente.

## Orden Pedagógico
1. Métricas definiciones y colección.
2. Capa caching (memoria) + invalidación.
3. Rate limiting (ej: 1 req/s por IP).
4. Streaming opcional.
5. Autenticación con token.

## Setup del Proyecto

> ### Inicio Rápido GUI
> Ver [Inicio Rápido GUI con Extensión ESP-IDF](../doc/setup.md#inicio-rapido-con-extension-esp-idf) para pasos de configuración GUI.
> Usar ejemplo: `$IDF_PATH/examples/openthread/ot_cli`.

### 1. Crear proyecto desde ejemplo ESP-IDF
```bash
idf.py create-project-from-example "$IDF_PATH/examples/openthread/ot_cli" lab07
cd lab07
```

### 2. Añadir código base CoAP + sensor + observabilidad features

**Base CoAP + sensor igual que Lab 5**, luego añadir caching, rate limiting y métricas.

**Añadir estructuras para caching y rate limiting** en `main/coap_demo.c`:
```c
#include <time.h>

// Cache para sensor data (5s TTL)
typedef struct {
    sensor_data_t data;
    time_t timestamp;
} sensor_cache_t;

static sensor_cache_t sensor_cache = {0};

// Rate limiting simple (por IP, 1 req/s)
#define MAX_CLIENTS 10
typedef struct {
    struct in6_addr ip;
    time_t last_request;
    int request_count;
} client_rate_limit_t;

static client_rate_limit_t rate_limits[MAX_CLIENTS] = {0};
```

**Función de rate limiting**:
```c
static bool check_rate_limit(const struct in6_addr *client_ip) {
    time_t now = time(NULL);
    
    for (int i = 0; i < MAX_CLIENTS; i++) {
        if (memcmp(&rate_limits[i].ip, client_ip, sizeof(struct in6_addr)) == 0) {
            if (now - rate_limits[i].last_request < 1) { // 1s limit
                rate_limits[i].request_count++;
                if (rate_limits[i].request_count > 5) { // burst limit
                    return false;
                }
            } else {
                rate_limits[i].request_count = 1;
            }
            rate_limits[i].last_request = now;
            return true;
        }
    }
    
    // New client
    for (int i = 0; i < MAX_CLIENTS; i++) {
        if (rate_limits[i].last_request == 0) {
            memcpy(&rate_limits[i].ip, client_ip, sizeof(struct in6_addr));
            rate_limits[i].last_request = now;
            rate_limits[i].request_count = 1;
            return true;
        }
    }
    return false; // Too many clients
}
```

**Modificar handlers para caching y rate limiting** (ejemplo en handle_sensor):
```c
static void handle_sensor(coap_context_t *ctx, coap_resource_t *resource,
                          coap_session_t *session, coap_pdu_t *request,
                          coap_binary_t *token, coap_string_t *query,
                          coap_pdu_t *response)
{
    char payload[128];
    size_t len;
    time_t now = time(NULL);
    coap_address_t *client_addr = coap_session_get_addr_remote(session);

    if (request->code != COAP_REQUEST_GET) {
        response->code = COAP_RESPONSE_CODE_METHOD_NOT_ALLOWED;
        return;
    }

    // Rate limiting
    if (!check_rate_limit(&client_addr->addr.sin6.sin6_addr)) {
        response->code = COAP_RESPONSE_CODE_TOO_MANY_REQUESTS;
        ESP_LOGW(TAG, "Rate limit exceeded for client");
        return;
    }

    // Caching (5s TTL)
    if (now - sensor_cache.timestamp > 5) {
        read_sensor_mock(&sensor_cache.data);
        sensor_cache.timestamp = now;
        ESP_LOGI(TAG, "Sensor cache updated");
    } else {
        ESP_LOGI(TAG, "Sensor cache hit");
    }

    len = snprintf(payload, sizeof(payload),
                   "{\"temp\":%.1f,\"hum\":%.1f,\"ts\":%u,\"seq\":%u}",
                   sensor_cache.data.temperature,
                   sensor_cache.data.humidity,
                   sensor_cache.data.timestamp,
                   sensor_cache.data.sequence);

    response->code = COAP_RESPONSE_CODE_CONTENT;
    coap_add_data_blocked_response(resource, session, request, response,
                                   token, COAP_MEDIATYPE_APPLICATION_JSON, 0,
                                   len, (const uint8_t *)payload);
}
```

**Añadir endpoint `/metrics`** para métricas básicas:
```c
static void handle_metrics(coap_context_t *ctx, coap_resource_t *resource,
                           coap_session_t *session, coap_pdu_t *request,
                           coap_binary_t *token, coap_string_t *query,
                           coap_pdu_t *response)
{
    char payload[256];
    size_t len;

    if (request->code != COAP_REQUEST_GET) {
        response->code = COAP_RESPONSE_CODE_METHOD_NOT_ALLOWED;
        return;
    }

    // Métricas simples (extender según necesidades)
    len = snprintf(payload, sizeof(payload),
                   "{\"uptime\":%u,\"heap_free\":%u,\"light_state\":%d}",
                   esp_log_timestamp() / 1000, esp_get_free_heap_size(), light_on);

    response->code = COAP_RESPONSE_CODE_CONTENT;
    coap_add_data_blocked_response(resource, session, request, response,
                                   token, COAP_MEDIATYPE_APPLICATION_JSON, 0,
                                   len, (const uint8_t *)payload);
}

// Registrar en coap_server_task
coap_resource_t *metrics_resource = coap_resource_init(coap_make_str_const("metrics"), 0);
coap_register_handler(metrics_resource, COAP_REQUEST_GET, handle_metrics);
coap_add_resource(ctx, metrics_resource);
```

### 3. Configurar settings

**Usar mismo `sdkconfig` que Lab 5**, sin cambios adicionales.

**Build y flash:**
```bash
idf.py set-target esp32c6
idf.py build
idf.py flash
idf.py monitor
```
