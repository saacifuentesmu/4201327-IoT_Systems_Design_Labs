# Lab 4 — Sensor Integration and Dashboards

## Objetivos
- Integrar sensor físico (I2C) o mock estructurado en red Thread.
- Exponer lectura vía CoAP JSON.
- Gestionar energía (sleep entre muestras) y medir duty cycle.
- Construir dashboard mínimo (Flask o stack elegido) lectura + control `/light`.

## Contexto
Conectar conceptos teóricos de integración de sensores y gestión de energía con la implementación práctica de adquisición de datos de sensores en redes Thread, exposición de API JSON y dashboards de monitoreo basados en web para dispositivos IoT.

## Orden Pedagógico
1. Driver / mock sensor.
2. Endpoint `/sensor` JSON estable.
3. PM básico (sleep) y logs timestamps.
4. Servicio recolector (polling o observe ya existente) → almacenar histórico.
5. Dashboard: tabla + último valor + toggle.

## Setup del Proyecto

### 1. Continuar con el proyecto de Lab 3

Este laboratorio continúa desarrollando el proyecto iniciado en Lab 3. Asegúrate de tener el proyecto `lab03` (o equivalente) abierto en VS Code.

### 2. Añadir código base CoAP + sensor físico/mock estructurado + PM básico

**Base CoAP igual que Lab 3**, luego añadir sensor estructurado y power management.

**Añadir estructuras de sensor** en `main/coap_demo.c` (después de defines):
```c
typedef struct {
    float temperature;
    float humidity;
    uint32_t timestamp;
    uint32_t sequence;
} sensor_data_t;

static sensor_data_t current_sensor_data = {0};
```

**Función mock de sensor** (simula I2C, reemplazar con driver real si hay sensor físico):
```c
static void read_sensor_mock(sensor_data_t *data) {
    // Simular lectura de sensor I2C (ej: SHT30)
    data->temperature = 20.0f + (esp_random() % 100) / 10.0f; // 20-30°C
    data->humidity = 40.0f + (esp_random() % 400) / 10.0f;    // 40-80%
    data->timestamp = esp_log_timestamp();
    data->sequence++;
}
```

**Modificar `handle_sensor`** para usar datos estructurados:
```c
static void handle_sensor(coap_context_t *ctx, coap_resource_t *resource,
                           coap_session_t *session, coap_pdu_t *request,
                           coap_binary_t *token, coap_string_t *query,
                           coap_pdu_t *response)
{
    char payload[128];
    size_t len;

    if (request->code != COAP_REQUEST_GET) {
        response->code = COAP_RESPONSE_CODE_METHOD_NOT_ALLOWED;
        return;
    }

    // Leer sensor antes de responder
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
}
```

**Añadir tarea de PM** en `main/coap_demo.c`:
```c
static void sensor_pm_task(void *pvParameters)
{
    while (1) {
        ESP_LOGI(TAG, "Sensor reading active");
        read_sensor_mock(&current_sensor_data);

        // Sleep entre muestras (30s para demo, ajustar según duty cycle)
        ESP_LOGI(TAG, "Entering light sleep for 30s");
        esp_sleep_enable_timer_wakeup(30 * 1000000); // 30s
        esp_light_sleep_start();

        ESP_LOGI(TAG, "Woke up from sleep");
    }
}

void start_sensor_pm(void)
{
    xTaskCreate(sensor_pm_task, "sensor_pm", 2048, NULL, 4, NULL);
}
```

**Llamar `start_sensor_pm()`** en `main/main.c` después de `start_coap_server()`.

### 3. Configurar settings para PM

**Actualizar `sdkconfig`** (añadir a configuraciones base):
```bash
# Power Management
CONFIG_PM_ENABLE=y
CONFIG_PM_DFS_INIT_AUTO=y
CONFIG_PM_LIGHT_SLEEP=y

# I2C (si usas sensor real)
CONFIG_I2C_ENABLED=y
```

**Build y flash:**
```bash
idf.py set-target esp32c6
idf.py build
idf.py flash
idf.py monitor
### 4. Construir Dashboard Mínimo

**Crear dashboard simple con Flask** (en el host PC):

**Instalar dependencias:**
```bash
pip install flask requests
```

**Crear `dashboard.py`:**
```python
from flask import Flask, render_template_string, request
import requests
import time

app = Flask(__name__)

# Configurar IPv6 del nodo Thread (obtener con ipaddr en CLI)
NODE_IP = "fd11:22:33:0:0:0:0:1"  # Reemplazar con IP real del nodo
COAP_PORT = 5683

def get_sensor_data():
    try:
        # Usar CoAP client para obtener datos
        import subprocess
        result = subprocess.run([
            "python", "tools/coap_client.py",
            "--host", NODE_IP, "get", "/sensor"
        ], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            # Parsear JSON (simplificado)
            data = result.stdout.strip()
            return data
        return "{}"
    except:
        return "{}"

def control_light(state):
    try:
        import subprocess
        result = subprocess.run([
            "python", "tools/coap_client.py",
            "--host", NODE_IP, "put", "/light", str(state)
        ], capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except:
        return False

@app.route('/')
def dashboard():
    sensor_data = get_sensor_data()
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>IoT Lab Dashboard</title>
        <meta http-equiv="refresh" content="5">
    </head>
    <body>
        <h1>IoT Sensor Dashboard</h1>
        <div id="sensor-data">{{ sensor_data }}</div>
        <h2>Control Luz</h2>
        <button onclick="controlLight(1)">Encender</button>
        <button onclick="controlLight(0)">Apagar</button>
        <script>
        function controlLight(state) {
            fetch('/control_light', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({state: state})
            });
        }
        </script>
    </body>
    </html>
    ''', sensor_data=sensor_data)

@app.route('/control_light', methods=['POST'])
def control_light_endpoint():
    data = request.get_json()
    state = data.get('state', 0)
    control_light(state)
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

**Ejecutar dashboard:**
```bash
python dashboard.py
```

Abrir http://localhost:5000 en navegador para ver dashboard con datos en tiempo real y control de luz.

## Entregables
- Endpoint `/sensor` JSON funcional con datos estructurados (temp, hum, ts, seq)
- Logs de power management (sleep/wake cycles)
- Dashboard web funcional con polling de sensor y control de luz
- Medidas de duty cycle y consumo estimado