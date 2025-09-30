# Lab 8 — Consolidación & Hardening (Integración Final)

## Objetivos
- Pruebas end-to-end automatizadas (script).
- Mini pentest: intento join no autorizado / CoAP inválido.
- Stress test ligero (ráfaga CoAP 20 req). 
- Documentación final + video demo.

## Contexto
Sintetizando todo el conocimiento teórico y práctico anterior, este laboratorio consolida el desarrollo de sistemas IoT con pruebas integrales, fortalecimiento de seguridad y documentación lista para producción.

## Orden Pedagógico
1. Definir casos test E2E.
2. Script automatizado (latencia, éxito, pérdida).
3. Stress test y registro recursos.
4. Prueba OTA adicional v3 rápida.
5. Hardening residual (ajuste token, límites).

## Setup del Proyecto

> ### Inicio Rápido GUI
> Ver [Inicio Rápido GUI con Extensión ESP-IDF](../doc/setup.md#inicio-rapido-con-extension-esp-idf) para pasos de configuración GUI.
> Usar ejemplo: `$IDF_PATH/examples/openthread/ot_cli`.

### 1. Crear proyecto desde ejemplo ESP-IDF
```bash
idf.py create-project-from-example "$IDF_PATH/examples/openthread/ot_cli" lab08
cd lab08
```

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
