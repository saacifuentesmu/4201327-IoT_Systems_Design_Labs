# Lab 11 — Seguridad y OTA (MCUboot) — Curso IoT ESP32‑C6

## Objetivos
- Repasar fundamentos de seguridad en Thread y commissioning.
- Firmar y actualizar una aplicación Zephyr usando MCUboot en ESP32‑C6.

## Pasos
1) Habilitar MCUboot vía sysbuild o con `CONFIG_BOOTLOADER_MCUBOOT=y`.
2) Compilar bootloader e imágenes de app; flashear el bootloader una vez.
3) Habilitar firmado de imagen; generar una llave de prueba y firmar.
4) Flashear la imagen firmada; verificar el arranque.
5) Extensión: experimentar con tokens de commissioning de OpenThread (PSKd) y join por CLI.

## Verificación
- Los logs de arranque muestran MCUboot y versión de la app; actualización a nueva imagen firmada completada.
