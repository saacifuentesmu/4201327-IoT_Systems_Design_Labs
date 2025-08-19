# Lab 04 — PHY 802.15.4 y sniffing — Curso IoT ESP32‑C6

## Objetivos
- Entender canales 2.4 GHz y modulación usada por 802.15.4 en el contexto IoT.
- Capturar tráfico Thread con un sniffer y analizar en Wireshark.

## Opciones de hardware
- Dongle USB nRF52840 con plugin nRF Sniffer para 802.15.4.
- Sniffer basado en ESP si está disponible; o usar un SDR.

## Pasos
1) Configurar canal Thread (ej., 20) en tus nodos.
2) Iniciar sniffer en el mismo canal; grabar pcapng.
3) Aplicar filtro de visualización Wireshark: `wpan || 6lowpan || thread`.
4) Identificar tipos de trama: Beacon, Data, Ack, MAC Command.
5) Medir cambios RSSI con distancia; registrar valores.

## Verificación
- Captura corta con tramas anotadas y tabla RSSI.
