# Lab 05 — Operaciones MAC 802.15.4

## Objetivos
- Observar escaneos, asociaciones y tramas de comandos MAC.
- Experimentar con umbral CCA y comportamiento de backoff.

## Pasos
1) Usar CLI para escaneo de energía: `ot scan energy 11 26 3`
2) Escaneo activo: `ot scan active`
3) Asociarse/unirse y observar tramas MAC Command en la captura.
4) Cambiar el umbral CCA vía Kconfig `CONFIG_IEEE802154_ESP32_CCA_THRESHOLD` y reconstruir.
5) Comparar trazas y ocupación de canal.

## Verificación
- Informe comparativo antes/después con capturas de pantalla.
