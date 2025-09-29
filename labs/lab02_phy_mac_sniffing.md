# Lab 2 — PHY + MAC + Sniffing (Fusión Labs 04 + 05)

## Objetivos
- Comprender canalización 2.4 GHz y tramas 802.15.4.
- Capturar y clasificar Beacon, Data, Ack, MAC Command.
- Evaluar impacto de CCA threshold y backoff.

## Contexto
Aplicando conceptos teóricos de las capas PHY y MAC de IEEE 802.15.4, este laboratorio demuestra análisis práctico de tramas y gestión de canales en redes de sensores inalámbricas.

## Orden Pedagógico
1. Revisión rápida pcap Lab 1.
2. Espectro y canales (canal elegido vs interferencia).
3. Sniffing y clasificación de tramas.
4. Escaneos energy/active y tabla comparativa.
5. Ajuste `CONFIG_OPENTHREAD_RADIO_CCA_THRESHOLD` en sdkconfig y rebuild.

## Setup del Proyecto

### 1. Crear proyecto desde ejemplo ESP-IDF
```bash
idf.py create-project-from-example "$IDF_PATH/examples/openthread/ot_cli" lab02
cd lab02
```

### 2. Añadir código base CoAP (igual que Lab 1)
Sigue los pasos 2 de Lab 1 para añadir el servidor CoAP básico.

### 3. Configurar settings para sniffing

**Actualizar `sdkconfig`** con configuraciones base (igual que Lab 1), luego configurar CCA threshold:
```bash
# Después del setup base, ajustar CCA threshold
idf.py menuconfig
# Navegar a: Component config → OpenThread → Radio Settings
# Ajustar CONFIG_OPENTHREAD_RADIO_CCA_THRESHOLD (valor por defecto: -75 dBm)
# Recomendado: probar -70 o -80 para comparación
```

**Build y flash:**
```bash
idf.py set-target esp32c6
idf.py build
idf.py flash
idf.py monitor
```
