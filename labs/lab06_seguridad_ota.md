# Lab 6 — Seguridad & OTA

## Objetivos
- Threat model básico (activos, amenazas, controles iniciales).
- Integrar MCUboot y firma de imágenes.
- Realizar actualización v1 → v2 (cambio visible: versión en log).
- Documentar pipeline de actualización segura.

## Contexto
Aplicando principios de seguridad y mecanismos de actualización over-the-air aprendidos en teoría, este laboratorio asegura actualizaciones de firmware con firma criptográfica e implementa pipelines de despliegue seguros.

## Setup del Proyecto

### 1. Crear proyecto desde ejemplo ESP-IDF

Usa la extensión ESP-IDF en VS Code:
1. Presiona `Ctrl+Shift+P` para abrir la paleta de comandos.
2. Busca y ejecuta `ESP-IDF: Show Examples` seleccionando la versión del ESP-IDF.
3. Selecciona `protocols/https_server/advanced_https_ota` (Advanced HTTPS OTA Example).
4. Selecciona la carpeta para crear el proyecto.

### 2. Configurar MCUboot y firma de imágenes

**Habilitar MCUboot** en el proyecto:
```bash
# Instalar dependencias si necesario
pip install imgtool

# Generar clave RSA para firma
imgtool keygen -k signing_key.pem -t rsa-2048

# Configurar MCUboot en menuconfig
idf.py menuconfig
# Component config → MCUboot Config → Enable MCUboot
# Security → Enable signature verification
# Configurar particiones para OTA (bootloader, primary, secondary)
```

**Añadir versión visible** en `main/main.c` (modificar app_main):
```c
void app_main(void) {
    ESP_LOGI(TAG, "IoT Lab Firmware Version: 1.0.0");
    // ... resto del código
}
```

### 3. Generar imágenes firmadas

**Construir imagen v1:**
```bash
idf.py build
imgtool sign --key signing_key.pem --header-size 0x200 --align 4 --version 1.0.0 --pad-header build/iot_lab_base.bin build/iot_lab_base_v1_signed.bin
```

**Para v2, cambiar versión en código:**
```c
ESP_LOGI(TAG, "IoT Lab Firmware Version: 2.0.0");
```
```bash
idf.py build
imgtool sign --key signing_key.pem --header-size 0x200 --align 4 --version 2.0.0 --pad-header build/iot_lab_base.bin build/iot_lab_base_v2_signed.bin
```

**Flash imagen v1:**
```bash
idf.py set-target esp32c6
idf.py flash --bin build/iot_lab_base_v1_signed.bin
idf.py monitor
```

**Para OTA, subir v2 al servidor HTTPS y trigger update desde dispositivo.**

**Flash imagen v1:**
```bash
idf.py set-target esp32c6
idf.py flash --bin build/iot_lab_base_v1_signed.bin
idf.py monitor
```

### 4. Configurar servidor HTTPS OTA

**Crear servidor HTTPS simple** (para demo, usar HTTP en producción usar HTTPS):

**Instalar dependencias:**
```bash
pip install flask
```

**Crear `ota_server.py`:**
```python
from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route('/firmware/<version>')
def serve_firmware(version):
    filename = f"build/iot_lab_base_{version}_signed.bin"
    if os.path.exists(filename):
        return send_file(filename, as_attachment=True)
    return "Firmware not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

**Ejecutar servidor:**
```bash
python ota_server.py
```

### 5. Implementar cliente OTA en dispositivo

**Añadir código OTA** en `main/main.c`:

```c
#include "esp_https_ota.h"
#include "esp_http_client.h"

// Función para OTA
static void perform_ota(const char *url)
{
    ESP_LOGI(TAG, "Starting OTA from: %s", url);

    esp_http_client_config_t config = {
        .url = url,
        .cert_pem = NULL, // En producción usar certificado
        .timeout_ms = 5000,
    };

    esp_err_t ret = esp_https_ota(&config);
    if (ret == ESP_OK) {
        ESP_LOGI(TAG, "OTA successful, restarting...");
        esp_restart();
    } else {
        ESP_LOGE(TAG, "OTA failed: %s", esp_err_to_name(ret));
    }
}

// Endpoint CoAP para trigger OTA
static void handle_ota(coap_context_t *ctx, coap_resource_t *resource,
                       coap_session_t *session, coap_pdu_t *request,
                       coap_binary_t *token, coap_string_t *query,
                       coap_pdu_t *response)
{
    if (request->code != COAP_REQUEST_POST) {
        response->code = COAP_RESPONSE_CODE_METHOD_NOT_ALLOWED;
        return;
    }

    // Extraer URL de payload (simplificado)
    char url[256] = "http://192.168.1.100:8080/firmware/v2"; // IP del servidor OTA

    response->code = COAP_RESPONSE_CODE_CHANGED;
    // Trigger OTA en tarea separada
    xTaskCreate(ota_task, "ota", 4096, (void *)url, 5, NULL);
}

static void ota_task(void *param)
{
    const char *url = (const char *)param;
    vTaskDelay(1000 / portTICK_PERIOD_MS); // Delay para responder CoAP
    perform_ota(url);
    vTaskDelete(NULL);
}

// Registrar recurso /ota
ota_resource = coap_resource_init(coap_make_str_const("ota"), 0);
coap_register_handler(ota_resource, COAP_REQUEST_POST, handle_ota);
coap_add_resource(ctx, ota_resource);
```

### 6. Realizar upgrade v1→v2

**Desde PC, trigger OTA:**
```bash
# Trigger upgrade desde PC
python tools/coap_client.py --host [IPv6 del nodo Thread] post /ota "upgrade"

# O desde CLI Thread en otro nodo
coap post [IPv6 del servidor] /ota upgrade
```

**Verificar upgrade:**
- Logs mostrarán "IoT Lab Firmware Version: 1.0.0" inicialmente
- Después de OTA: "IoT Lab Firmware Version: 2.0.0"
- MCUboot logs mostrarán verificación de firma y upgrade

### 7. Threat model básico

**Activos:**
- Firmware del dispositivo
- Datos de sensor
- Credenciales de red Thread

**Amenazas:**
- Ataque man-in-the-middle en OTA
- Firmware malicioso
- Acceso físico al dispositivo

**Controles:**
- Firma criptográfica de firmware
- Verificación de integridad con MCUboot
- Actualizaciones solo desde fuentes autorizadas

## Entregables
- Modelo de amenazas básico (activos, amenazas, controles)
- Imágenes firmware v1 y v2 firmadas con clave RSA
- Logs de MCUboot mostrando verificación de firma
- Logs de upgrade OTA exitoso v1→v2 con cambio visible de versión
- Documento de pipeline de actualización segura
