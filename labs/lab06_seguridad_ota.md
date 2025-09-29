# Lab 6 — Seguridad & OTA (Lab 11)

## Objetivos
- Threat model básico (activos, amenazas, controles iniciales).
- Integrar MCUboot y firma de imágenes.
- Realizar actualización v1 → v2 (cambio visible: versión en log).
- Documentar pipeline de actualización segura.

## Contexto
Aplicando principios de seguridad y mecanismos de actualización over-the-air aprendidos en teoría, este laboratorio asegura actualizaciones de firmware con firma criptográfica e implementa pipelines de despliegue seguros.

## Orden Pedagógico
1. Modelo de amenazas (tabla activos/amenazas).
2. Habilitar MCUboot (sysbuild / config).
3. Generar clave y firmar imagen v1.
4. Crear v2 con cambio de versión.
5. Validar logs arranque y rollback opcional.

## Setup del Proyecto

### 1. Crear proyecto desde ejemplo ESP-IDF con OTA
```bash
idf.py create-project-from-example "$IDF_PATH/examples/protocols/https_server/advanced_https_ota" lab06
cd lab06
```

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
