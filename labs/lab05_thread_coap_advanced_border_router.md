# Lab 5 — Thread/CoAP Advanced & Border Router

## Objetivos
- Implementar un Border Router (OTBR) con RCP ESP32-C6.
- Acceder nodos Thread desde LAN (ping, CoAP).
- Añadir CoAP Observe al recurso `/sensor`.
- Pruebas CoAP network-based con Python client.
- (Opcional) Introducir MQTT (broker local) como comparación pub/sub.

## Contexto
Extendiendo el conocimiento en clase de border routers y patrones de aplicación, este laboratorio implementa un Border Router Thread y demuestra patrones publish-subscribe usando CoAP Observe para streaming de datos IoT en tiempo real, habilitando acceso network desde PC.

## Setup del Proyecto

### 1. Crear proyecto RCP separado

Para este laboratorio, crea un proyecto separado para el Radio Co-Processor (RCP) que se conectará al Border Router corriendo en el host:

Usa la extensión ESP-IDF en VS Code:
1. Presiona `Ctrl+Shift+P` para abrir la paleta de comandos.
2. Busca y ejecuta `ESP-IDF: Show Examples` seleccionando la versión del ESP-IDF.
3. Selecciona `openthread/ot_rcp` (OpenThread RCP Example).
4. Selecciona la carpeta para crear el proyecto (ej. `lab05_rcp`).

### 2. Configurar para modo RCP (sin código adicional, RCP no ejecuta aplicación)

El RCP (Radio Co-Processor) no ejecuta código de aplicación; solo maneja la radio Thread.
El CoAP server con observe corre en los nodos CLI (de Labs anteriores).

### 3. Configurar settings

**Configurar sdkconfig para RCP:**
```bash
# El ejemplo ot_rcp ya tiene configuraciones base
# Ajustar si necesario:
idf.py menuconfig
# Verificar: CONFIG_OPENTHREAD_RCP=y
# Deshabilitar CLI y FTD ya que es RCP puro
```

**Build y flash:**
```bash
idf.py set-target esp32c6
idf.py build
idf.py flash
# Este dispositivo actuará como RCP para OTBR corriendo en el host
```

### 4. Configurar OTBR y probar conectividad

Sigue las instrucciones de OTBR para configurar el Border Router en tu host. Una vez configurado, los nodos Thread serán accesibles desde la LAN.

### 5. Probar CoAP con cliente Python (Network-based)

Ahora que el Border Router está activo, puedes usar el cliente Python para acceder a los nodos Thread desde tu PC.

**Instalar dependencias en el host:**
```bash
pip install aiocoap
```

**Uso del cliente Python:**
```bash
# Obtener estado del sensor
python tools/coap_client.py --host [IPv6 del nodo Thread] get /sensor

# Obtener estado de la luz
python tools/coap_client.py --host [IPv6 del nodo Thread] get /light

# Cambiar estado de la luz (0=off, 1=on)
python tools/coap_client.py --host [IPv6 del nodo Thread] put /light 1
```

**Nota:** Las direcciones IPv6 Thread ahora son routables a través del Border Router. Usa `ipaddr` en la CLI Thread para obtener las direcciones.
### 6. Añadir CoAP Observe al recurso `/sensor`

**Modificar `handle_sensor`** para soportar observe (en nodos Thread):

Añadir en `main/coap_demo.c`:
```c
// Añadir variable global para notificaciones
static coap_resource_t *sensor_resource = NULL;
static sensor_data_t last_notified_data = {0};

// Modificar handle_sensor para observe
static void handle_sensor(coap_context_t *ctx, coap_resource_t *resource,
                          coap_session_t *session, coap_pdu_t *request,
                          coap_binary_t *token, coap_string_t *query,
                          coap_pdu_t *response)
{
    char payload[128];
    size_t len;

    if (request->code == COAP_REQUEST_GET) {
        // Leer sensor
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

        // Para observe, recordar último valor
        last_notified_data = current_sensor_data;
    } else if (request->code == COAP_REQUEST_OBSERVE) {
        // Manejar observe registration/deregistration
        coap_observe_add(resource, session, token);
        response->code = COAP_RESPONSE_CODE_CONTENT;
    } else {
        response->code = COAP_RESPONSE_CODE_METHOD_NOT_ALLOWED;
    }
}

// Función para enviar notificaciones observe
static void notify_sensor_observers(void)
{
    if (sensor_resource) {
        char payload[128];
        size_t len;

        // Solo notificar si datos cambiaron significativamente
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

**Modificar tarea de sensor** para notificar observers:
```c
static void sensor_pm_task(void *pvParameters)
{
    while (1) {
        ESP_LOGI(TAG, "Sensor reading active");
        read_sensor_mock(&current_sensor_data);

        // Notificar observers si hay cambios
        notify_sensor_observers();

        ESP_LOGI(TAG, "Entering light sleep for 30s");
        esp_sleep_enable_timer_wakeup(30 * 1000000);
        esp_light_sleep_start();

        ESP_LOGI(TAG, "Woke up from sleep");
    }
}
```

### 7. Pruebas CoAP Observe con cliente network

**Probar observe desde PC:**
```bash
# Registrar para observe (dejará corriendo)
python tools/coap_client.py --host [IPv6 del nodo Thread] observe /sensor

# En otra terminal, trigger notificaciones cambiando sensor (o esperando cambios naturales)
# Las notificaciones aparecerán automáticamente cuando el sensor cambie
```

**Medir métricas de entrega:**
- Ratio de éxito de notificaciones
- Latencia entre cambio de sensor y recepción de notificación
- Overhead de observe vs polling

## Entregables
- Border Router RCP funcional con OTBR corriendo
- Logs de conectividad LAN→Thread (ping, CoAP desde PC)
- Endpoint `/sensor` con soporte CoAP observe
- Demo de observe con cliente network mostrando notificaciones en tiempo real
- Métricas de entrega (ratio éxito, latencia notificación)