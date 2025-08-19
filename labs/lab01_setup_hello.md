# Lab 01 — Ecosistema embebido y RTOS para IoT

## Objetivos de Aprendizaje IoT
- Entender las diferencias entre sistemas embebidos tradicionales y sistemas IoT
- Configurar toolchain profesional para desarrollo IoT (Zephyr/west)
- Explorar el concepto de RTOS y su importancia en sistemas constreñidos
- Construir y ejecutar aplicaciones básicas en hardware real

## Conceptos IoT Cubiertos
- **Device constraints**: memoria, CPU, energía, conectividad
- **RTOS vs OS tradicional**: scheduling, memory management, real-time guarantees
- **Toolchain profesional**: cross-compilation, debugging, deployment

## Herramientas Utilizadas
- **Zephyr RTOS**: Sistema operativo profesional para IoT
- **ESP32‑C6 DevKitC**: Hardware representativo de dispositivos IoT modernos  
- **West**: Build system y package manager para Zephyr

## Ejemplos Base de Zephyr
- `samples/hello_world`: Verificación básica del toolchain
- `samples/basic/blinky`: GPIO y timing básico
- `samples/sensor/sensor_shell`: Introducción a drivers y shell

## Pasos del Laboratorio

### Parte A: Setup del Ecosistema (45 min)
1) **Verificar prerrequisitos** según `../setup.md`
   - Python venv activado
   - Zephyr SDK instalado 
   - west disponible

2) **Explorar la estructura de Zephyr**:
   ```bash
   ls zephyr/samples/          # Ecosistema de ejemplos
   ls zephyr/boards/espressif/ # Soporte para familia ESP32
   west boards | grep esp32c6  # Verificar nuestra placa
   ```

3) **Entender el workflow de desarrollo**:
   ```bash
   west build -b esp32c6_devkitc/esp32c6/hpcore zephyr/samples/hello_world
   west flash
   west espressif monitor
   ```

### Parte B: Aplicaciones Básicas (45 min)
4) **Hello World - Verificación básica**:
   - Observar startup sequence del RTOS
   - Identificar componentes: kernel, drivers, shell
   - Medir tiempo de boot y memory usage

5) **Blinky - GPIO y Timing**:
   - Modificar frecuencia de parpadeo en `prj.conf`
   - Entender device tree y abstracción de hardware
   - Observar scheduling determinístico

### Parte C: Exploración de Drivers (30 min)  
6) **Sensor shell — introducción a IoT**:
   ```bash
   west build -b esp32c6_devkitc zephyr/samples/sensor/sensor_shell -p
   ```
   - Explorar comando `sensor` en el shell
   - Entender abstracción de hardware para sensores
   - Simular lecturas de sensores internos (temperatura del die)

## Entregables

### Reporte Técnico: "RTOS vs OS Tradicional para IoT" (1-2 páginas)
**Estructura sugerida:**
1) **Comparación conceptual**: 
   - Memory footprint (Zephyr vs Linux)
   - Boot time observado vs typical Linux boot
   - Determinismo en scheduling (evidencia del blinky)

2) **Casos de uso IoT**:
   - ¿Cuándo usar RTOS vs Linux en sistemas IoT?
   - Trade-offs: features vs resources vs real-time

3) **Observaciones del laboratorio**:
   - Tiempo de compilación vs tiempo de boot
   - Memory usage reportado por west
   - Facilidad de cross-compilation

### Evidencia Práctica
- Screenshots de serial output de cada aplicación
- Logs del proceso de build/flash
- Modificación exitosa de blinky timing

## Para la Siguiente Clase
**Preparación**: Leer documentación de OpenThread en Zephyr:
- `zephyr/samples/net/openthread/README.rst`
- Conceptos: Thread vs WiFi vs Zigbee para mesh networking

**Reflexión**: ¿Qué ventajas podría tener una red mesh auto-configurable para sistemas IoT vs una red star tradicional?
