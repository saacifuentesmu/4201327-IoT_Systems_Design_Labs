# Lab 09 — Border Router (OTBR) con RCP ESP32‑C6

## Objetivos
- Conectar la red Thread a Ethernet/Wi‑Fi usando OTBR.
- Alcanzar nodos Thread desde tu laptop.

## Rutas
- A) Recomendado: Compilar RCP en ESP32‑C6: `samples/net/openthread/coprocessor` y ejecutar OTBR en Linux (Docker o nativo).
- B) Alternativa: Usar `samples/net/openthread/border_router` de Zephyr en hardware soportado.

## Pasos (Ruta A)
1) Compilar y flashear el RCP para `esp32c6_devkitc`.
2) Conectar el RCP al host Linux vía UART.
3) Instalar/ejecutar OTBR; apuntar al TTY del RCP; formar red.
4) Verificar ping desde LAN a la dirección global del nodo Thread vía BR.

## Verificación
- Funciona una petición CoAP de LAN a Thread (curl en laptop → BR → nodo).
