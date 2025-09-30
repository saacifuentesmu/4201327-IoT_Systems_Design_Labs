# Lab 4 — Border Router + Patrones de Aplicación

## Objetivos
- Implementar un Border Router (OTBR) con RCP ESP32-C6.
- Acceder nodos Thread desde LAN (ping, CoAP).
- Añadir CoAP Observe al recurso `/sensor`.
- (Opcional) Introducir MQTT (broker local) como comparación pub/sub.

## Contexto
Extendiendo el conocimiento en clase de border routers y patrones de aplicación, este laboratorio implementa un Border Router Thread y demuestra patrones publish-subscribe usando CoAP Observe para streaming de datos IoT en tiempo real.

## Orden Pedagógico
1. RCP build + OTBR docker / nativo.
2. Ver conectividad LAN→Thread.
3. CoAP Observe flujo (registro + notificaciones).
4. Métricas entrega (ratio y latencia notificación).
5. (Opcional) MQTT bridging.

## Setup del Proyecto

> ### Inicio Rápido GUI
> Ver [Inicio Rápido GUI con Extensión ESP-IDF](../doc/setup.md#inicio-rapido-con-extension-esp-idf) para pasos de configuración GUI.
> Usar ejemplo: `$IDF_PATH/examples/openthread/ot_rcp`.

### 1. Crear proyecto desde ejemplo ESP-IDF
```bash
idf.py create-project-from-example "$IDF_PATH/examples/openthread/ot_rcp" lab04
cd lab04
```

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
