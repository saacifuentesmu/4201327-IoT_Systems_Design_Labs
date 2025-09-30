# Lab 3 — 6LoWPAN + Routing & Resiliencia

## Objetivos
- Enumerar y clasificar direcciones IPv6 (link-local, mesh-local, ML-EID).
- Observar fragmentación 6LoWPAN.
- Evaluar re-attach y cambio de roles (líder, routers, children).

## Contexto
Traduciendo el entendimiento teórico de la capa de adaptación 6LoWPAN y los protocolos de enrutamiento Thread en observación práctica de direccionamiento IPv6, fragmentación de paquetes y mecanismos de resiliencia de red.

## Orden Pedagógico
1. Direcciones y prefijos.
2. Fragmentación forzada (payload > 80B CoAP PUT/POST ficticio).
3. MLE messages y re-attach inducido (mover nodo / apagar líder).
4. Medición tiempos convergencia.

## Setup del Proyecto

> ### Inicio Rápido GUI
> Ver [Inicio Rápido GUI con Extensión ESP-IDF](../doc/setup.md#inicio-rapido-con-extension-esp-idf) para pasos de configuración GUI.
> Usar ejemplo: `$IDF_PATH/examples/openthread/ot_cli`.

### 1. Crear proyecto desde ejemplo ESP-IDF
```bash
idf.py create-project-from-example "$IDF_PATH/examples/openthread/ot_cli" lab03
cd lab03
```

### 2. Añadir código base CoAP (igual que Lab 1) + endpoint para fragmentación

**Base CoAP igual que Lab 1**, luego añadir endpoint `/large` para forzar fragmentación 6LoWPAN:

**Añadir en `main/coap_demo.c`** (después de handle_sensor):
```c
static void handle_large(coap_context_t *ctx, coap_resource_t *resource,
                         coap_session_t *session, coap_pdu_t *request,
                         coap_binary_t *token, coap_string_t *query,
                         coap_pdu_t *response)
{
    // Payload > 80 bytes para forzar fragmentación 6LoWPAN
    const char *large_payload =
        "This is a large payload designed to exceed the 6LoWPAN MTU limit "
        "and force fragmentation. The payload contains more than 80 bytes "
        "of data to demonstrate how 6LoWPAN handles large packets by "
        "breaking them into smaller fragments for transmission over "
        "IEEE 802.15.4 networks. Fragmentation is essential for IoT "
        "applications that need to send larger data packets.";

    if (request->code != COAP_REQUEST_GET) {
        response->code = COAP_RESPONSE_CODE_METHOD_NOT_ALLOWED;
        return;
    }

    response->code = COAP_RESPONSE_CODE_CONTENT;
    coap_add_data_blocked_response(resource, session, request, response,
                                   token, COAP_MEDIATYPE_TEXT_PLAIN, 0,
                                   strlen(large_payload),
                                   (const uint8_t *)large_payload);
}
```

**Registrar el nuevo recurso** en coap_server_task (después de sensor_resource):
```c
coap_resource_t *large_resource = NULL;

// ...

large_resource = coap_resource_init(coap_make_str_const("large"), 0);
if (!large_resource) {
    ESP_LOGE(TAG, "Failed to create large resource");
    goto finish;
}
coap_register_handler(large_resource, COAP_REQUEST_GET, handle_large);
coap_add_resource(ctx, large_resource);
```

### 3. Configurar settings

**Usar mismo `sdkconfig` que Lab 1**, sin cambios adicionales.

**Build y flash:**
```bash
idf.py set-target esp32c6
idf.py build
idf.py flash
idf.py monitor
```
