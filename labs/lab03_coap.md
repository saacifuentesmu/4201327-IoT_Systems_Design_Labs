# Lab 03 — CoAP sobre Thread — Curso IoT ESP32‑C6

## Objetivos
- Ejecutar ejemplo CoAP sobre Thread entre dos placas ESP32-C6.
- Controlar LED vía CoAP y leer un sensor mock en el contexto del curso de IoT.

## Aplicación base
- `zephyr/samples/net/openthread/coap`

## Pasos
1) Construir servidor (FTD):
   - `prj.conf` por defecto habilita OpenThread.
   - Placa `esp32c6_devkitc`.
   - Compila y flashea el servidor.
2) Construir cliente para la misma placa y flashear.
3) Formar red en servidor vía shell.
4) En cliente, configurar mismo canal/PAN e iniciar; descubrir servidor con `ot discover` o usar dirección conocida.
5) Probar CoAP (endpoints por defecto en el ejemplo):
   - GET `/light`
   - PUT `/light` payload `1` (encendido) o `0` (apagado)
6) Extender servidor para agregar `/sensor` retornando un contador o valor mock.

## Verificación
- El cliente conmuta el LED del servidor.
- El cliente lee el valor de `/sensor`.

## Consejos
- Usa niveles de log para depurar.
- Captura con Wireshark para observar mensajes confirmables de CoAP.
