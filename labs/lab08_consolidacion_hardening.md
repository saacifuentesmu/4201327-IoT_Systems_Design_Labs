# Lab 8 — Consolidación & Hardening (Integración Final)

## Objetivos
- Pruebas end-to-end automatizadas (script).
- Mini pentest: intento join no autorizado / CoAP inválido.
- Stress test ligero (ráfaga CoAP 20 req). 
- Documentación final + video demo.

## Contexto
Sintetizando todo el conocimiento teórico y práctico anterior, este laboratorio consolida el desarrollo de sistemas IoT con pruebas integrales, fortalecimiento de seguridad y documentación lista para producción.

## Setup del Proyecto

### 1. Continuar con el proyecto de Lab 3

Este laboratorio continúa desarrollando el proyecto iniciado en Lab 3. Asegúrate de tener el proyecto `lab03` (o equivalente) abierto en VS Code.

### 2. Añadir código base completo + hardening (token auth)

**Base completa igual que Lab 7**, luego añadir autenticación simple con token.

**Añadir token auth** en `main/coap_demo.c` (después de defines):
```c
#define AUTH_TOKEN "iotlab2024"  // Token hardcoded para demo (en producción usar NVS o similar)

static bool check_auth_token(coap_pdu_t *request) {
    coap_opt_iterator_t opt_iter;
    coap_opt_t *token_option = coap_check_option(request, COAP_OPTION_URI_QUERY, &opt_iter);
    
    if (!token_option) {
        return false;
    }
    
    char token_str[32];
    size_t token_len = coap_opt_length(token_option);
    if (token_len >= sizeof(token_str)) {
        return false;
    }
    
    coap_opt_value(token_option, (uint8_t *)token_str);
    token_str[token_len] = '\0';
    
    // Check if token=AUTH_TOKEN
    if (strncmp(token_str, "token=", 6) == 0 && strcmp(token_str + 6, AUTH_TOKEN) == 0) {
        return true;
    }
    
    return false;
}
```

**Modificar handlers para requerir token** (ejemplo en handle_light):
```c
static void handle_light(coap_context_t *ctx, coap_resource_t *resource,
                         coap_session_t *session, coap_pdu_t *request,
                         coap_binary_t *token, coap_string_t *query,
                         coap_pdu_t *response)
{
    // Auth check
    if (!check_auth_token(request)) {
        response->code = COAP_RESPONSE_CODE_UNAUTHORIZED;
        ESP_LOGW(TAG, "Unauthorized access to /light");
        return;
    }

    // Rate limiting
    coap_address_t *client_addr = coap_session_get_addr_remote(session);
    if (!check_rate_limit(&client_addr->addr.sin6.sin6_addr)) {
        response->code = COAP_RESPONSE_CODE_TOO_MANY_REQUESTS;
        return;
    }

    // Original logic...
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

**Aplicar mismo check a handle_sensor y handle_metrics**.

### 3. Configurar settings finales

**Usar mismo `sdkconfig` que Lab 7**, añadir hardening:
```bash
# Security hardening
CONFIG_COMPILER_OPTIMIZATION_LEVEL_DEBUG=n
CONFIG_COMPILER_OPTIMIZATION_LEVEL_RELEASE=y
CONFIG_STACK_CHECK_NONE=n
CONFIG_STACK_CHECK_NORM=y
```

**Build y flash:**
```bash
idf.py set-target esp32c6
idf.py build
idf.py flash
idf.py monitor
```

### 4. Script de pruebas end-to-end automatizadas

**Usar la suite de pruebas desde `tools/test_e2e.py`** (ya incluido en el repositorio).

**Ejecutar pruebas:**
```bash
# Pruebas básicas
python tools/test_e2e.py fd11:22:33:0:0:0:0:1

# Con Border Router
python tools/test_e2e.py fd11:22:33:0:0:0:0:1 fd11:22:33:0:0:0:0:100
```

### 5. Mini pentest y hardening residual

**Pruebas de seguridad:**
```bash
# Intentar join no autorizado (desde dispositivo sin credenciales)
# En CLI Thread de dispositivo no autorizado:
dataset set active <dataset_hex_incorrecto>
ifconfig up
thread start
# Debería fallar

# CoAP requests inválidos
python tools/coap_client.py --host [IPv6] get /invalid_endpoint
python tools/coap_client.py --host [IPv6] put /light invalid_payload

# Stress test de recursos
# Ejecutar múltiples instancias del stress test
for i in {1..5}; do
    python tools/test_e2e.py fd11:22:33:0:0:0:0:1 &
done
```

### 6. Documentación final y video demo

**Estructura de documentación:**
- Arquitectura general del sistema
- APIs CoAP documentadas
- Guía de despliegue
- Troubleshooting común
- Métricas de rendimiento

**Video demo checklist:**
- Formación de red Thread
- Funcionalidad básica CoAP
- Dashboard en funcionamiento
- Border Router y acceso network
- OTA update
- Pruebas end-to-end
- Demo de seguridad (rate limiting, auth)

## Entregables
- Suite de pruebas automatizadas (`tools/test_e2e.py`) con métricas de latencia y éxito
- Reporte de pruebas end-to-end (ratio éxito, latencia promedio)
- Logs de stress test (ráfaga 20 req) y uso de recursos
- Resultados de mini pentest (intentos join no autorizado, CoAP inválido)
- Documentación final completa del sistema IoT
- Video demo mostrando funcionalidad completa y pruebas
