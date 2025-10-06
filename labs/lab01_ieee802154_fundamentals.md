# Lab 1 — IEEE 802.15.4 Fundamentals (PHY/MAC/Sniffing)

## Objetivos
- Comprender canalización 2.4 GHz y tramas 802.15.4.
- Capturar y clasificar Beacon, Data, Ack, MAC Command.
- Evaluar impacto de CCA threshold y backoff.

## Contexto
Introduciendo los fundamentos de las capas físicas y de enlace de IEEE 802.15.4, este laboratorio establece las bases para el desarrollo de redes IoT mediante análisis práctico de tramas y gestión de canales.

## Setup del Proyecto

### 1. Crear proyecto desde ejemplo ESP-IDF

Usa la extensión ESP-IDF en VS Code:
1. Presiona `Ctrl+Shift+P` para abrir la paleta de comandos.
2. Busca y ejecuta `ESP-IDF: Show Examples` seleccionando la versión del ESP-IDF.
3. Selecciona `ieee802154/ieee802154_cli` (IEEE802.15.4 Command Line Example).
4. Seleccione la carpeta para crear el proyecto.

### 2. Explorar el código del ejemplo IEEE 802.15.4

El ejemplo `ieee802154/ieee802154_cli` incluye código para comunicación básica IEEE 802.15.4. Examina los archivos principales en el directorio del proyecto creado:

- `main/esp_ieee802154_cli.c`: Punto de entrada del ejemplo CLI
- `components/cmd_ieee802154/ieee802154_cmd.c`: Implementación de comandos CLI

### 3. Build y flash del proyecto

El ejemplo usa configuraciones por defecto adecuadas para IEEE 802.15.4, incluyendo parámetros físicos como desviación de frecuencia según el estándar. No se requieren cambios en sdkconfig.

Usa la barra de herramientas ESP-IDF en VS Code:
1. Haz clic en **ESP-IDF: Establecer Objetivo** y selecciona `esp32c6`.
2. Haz clic en **ESP-IDF: Construir Proyecto**.
3. Conecta la ESP32-C6 y haz clic en **ESP-IDF: Flashear Dispositivo**.
4. Haz clic en **ESP-IDF: Monitorear Dispositivo**.

### 4. Explorar parámetros IEEE 802.15.4

Una vez en la consola del dispositivo, usa los comandos CLI del ejemplo (todos los comandos están documentados en `help`):

```bash
# Ver ayuda completa
help

# Configurar canal (11-26)
channel -s 15

# Ver canal actual
channel -g

# Configurar potencia de transmisión (-80 a -10 dBm)
txpower -s 10

# Ver potencia actual
txpower -g

# Configurar PAN ID
panid 0x1234

# Ver PAN ID
panid -g

# Configurar dirección corta
shortaddr 0x0001

# Ver dirección corta
shortaddr -g

# Configurar dirección extendida
extaddr 0xaa 0xbb 0xcc 0xdd 0x00 0x11 0x22 0x33

# Ver dirección extendida
extaddr -g
```

### 5. Comunicación entre dispositivos

**Configurar Dispositivo A (Coordinador):**
```bash
# Configurar PAN ID y direcciones
panid 0x1234
shortaddr 0x0001
channel -s 15

# Entrar en modo recepción
rx -r 1
```

**Configurar Dispositivo B (Nodo):**
```bash
# Configurar misma PAN ID, dirección diferente
panid 0x1234
shortaddr 0x0002
channel -s 15

# Transmitir datos al dispositivo A
tx 0x00 0x01 0x02 0x03  # Datos de ejemplo
```

**Verificar comunicación:**
- Dispositivo A debería recibir los datos transmitidos por B
- Intercambiar roles y probar transmisión bidireccional

### 6. Análisis de Espectro y Capa Física

**Análisis de espectro con Spectrum Analyzer:**
- Observa ocupación de canales 2.4GHz (canales 11-26, espaciados cada 5 MHz)
- Identifica interferencia de WiFi, Bluetooth, microwaves
- Mide ancho de canal (2 MHz), espaciado de canal (5 MHz) y ancho de banda RF

**Análisis de capa física:**
- Verifica frecuencia central de cada canal (ej. canal 11: 2405 MHz)
- Observa modulación O-QPSK y spreading DSSS
- Mide potencia de señal y relación señal-ruido (SNR)

### 7. Experimentos con CCA y Parámetros de Radio

**Ajustar CCA threshold y modo:**
```bash
# Ver configuración CCA actual
cca -g

# Configurar threshold (-60 dBm en el ejemplo)
cca -v -60

# Configurar modo CCA (1: ED, 2: carrier or ED, etc.)
cca -m 1
```

**Detección de energía:**
```bash
# Escanear energía por duración específica
ed -d 2
```

**Experimentos detallados:**

1. **Cambio de canales:** Prueba comunicación en diferentes canales
   ```bash
   # Cambiar a canal 11, 15, 20, 26
   channel -s 11
   channel -s 15
   # etc.
   ```

2. **Potencia de transmisión:** Varía txpower (-80 a -10 dBm)
   ```bash
   txpower -s -10  # Máxima potencia
   txpower -s -80  # Mínima potencia
   ```

3. **CCA threshold:** Ajusta sensibilidad
    ```bash
    cca -v -70  # Más sensible
    cca -v -80  # Menos sensible
    ```

4. **Backoff en CSMA-CA:** Configura dos dispositivos transmitiendo datos frecuentemente en el mismo canal. Observa en los logs si hay retransmisiones o delays debido a backoff. Compara con canal libre.

**Mediciones y análisis:**
- RSSI, LQI, PER, throughput
- Crea tabla comparativa de rendimiento
- Documenta impacto de interferencia ambiental
- Mide alcance vs potencia de transmisión

## Entregables
- Comparativa de CCA/canales + análisis de interferencia
- Tabla de mediciones de rendimiento (RSSI, LQI, PER, throughput)
- Análisis de espectro con identificación de interferencia
- Documentación de alcance vs potencia de transmisión
