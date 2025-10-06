# Lab 2 — 6LoWPAN + Routing & Resiliencia

## Objetivos
- Enumerar y clasificar direcciones IPv6 (link-local, mesh-local, ML-EID).
- Observar fragmentación 6LoWPAN.
- Evaluar re-attach y cambio de roles (líder, routers, children).

## Contexto
Aplicando conceptos teóricos de la capa de adaptación 6LoWPAN y los protocolos de enrutamiento Thread en observación práctica de direccionamiento IPv6, fragmentación de paquetes y mecanismos de resiliencia de red.

## Setup del Proyecto

### 1. Crear proyecto desde ejemplo ESP-IDF

Usa la extensión ESP-IDF en VS Code:
1. Presiona `Ctrl+Shift+P` para abrir la paleta de comandos.
2. Busca y ejecuta `ESP-IDF: Show Examples` seleccionando la versión del ESP-IDF.
3. Selecciona `openthread/ot_cli` (OpenThread CLI Example).
4. Selecciona la carpeta para crear el proyecto.

### 2. Explorar el código del ejemplo OpenThread CLI

El ejemplo `openthread/ot_cli` incluye código para CLI básica de Thread. Examina los archivos principales en el directorio del proyecto creado:

- `main/esp_ot_cli.c`: Punto de entrada del ejemplo CLI
- Componentes OpenThread para manejo de red Thread

### 3. Build y flash del proyecto

El ejemplo usa configuraciones por defecto adecuadas para Thread/6LoWPAN. No se requieren cambios en sdkconfig para este laboratorio básico.

Usa la barra de herramientas ESP-IDF en VS Code:
1. Haz clic en **ESP-IDF: Establecer Objetivo** y selecciona `esp32c6`.
2. Haz clic en **ESP-IDF: Construir Proyecto**.
3. Conecta la ESP32-C6 y haz clic en **ESP-IDF: Flashear Dispositivo**.
4. Haz clic en **ESP-IDF: Monitorear Dispositivo**.

### 4. Explorar comandos CLI de Thread/6LoWPAN

Una vez en la consola del dispositivo, usa los comandos CLI del ejemplo (todos los comandos están documentados en `help`):

```bash
# Ver ayuda completa
help

# Ver estado de la interfaz
ifconfig

# Ver direcciones IPv6 asignadas
ipaddr

# Ver direcciones multicast
ipmaddr

# Ver tabla de routers
router table

# Ver tabla de vecinos
neighbor table

# Ver rutas
routes
```

### 5. Formación de red Thread básica

**Configurar Dispositivo A (Líder):**
```bash
# Crear nuevo dataset de red
dataset init new

# Configurar canal y PAN ID
dataset channel 15
dataset panid 0x1234

# Configurar master key
dataset masterkey 00112233445566778899aabbccddeeff

# Activar dataset
dataset commit active

# Iniciar interfaz y Thread
ifconfig up
thread start
```

**Configurar Dispositivo B (Router/Child):**
```bash
# Obtener dataset del líder (en dispositivo A)
# dataset active -x

# Copiar el dataset hexadecimal al dispositivo B
dataset set active <dataset_hex_del_líder>

# Iniciar interfaz y Thread
ifconfig up
thread start
```

**Verificar formación de red:**
- Ambos dispositivos deberían unirse a la red Thread
- Usar `state` para ver roles (leader, router, child)
- Usar `ipaddr` para ver direcciones IPv6 asignadas

### 6. Análisis de Direcciones IPv6 en 6LoWPAN

**Tipos de direcciones a observar:**

1. **Link-local**: Prefijo `fe80::/10`, usado para comunicación local
2. **Mesh-local**: Prefijo derivado del dataset (ej. `fd11:22:33::/64`), usado dentro de la mesh
3. **ML-EID (Mesh-Local EID)**: Dirección única del dispositivo en la mesh

**Comandos para análisis:**
```bash
# Ver todas las direcciones
ipaddr

# Ver direcciones multicast (incluyendo All-Thread-Nodes)
ipmaddr

# Ver detalles del dataset (para entender prefijos)
dataset active
```

**Análisis:**
- Documenta cada tipo de dirección y su propósito
- Observa cómo cambian las direcciones al unirse a diferentes redes
- Compara direcciones entre dispositivos en la misma red

### 7. Observación de Fragmentación 6LoWPAN

**Forzar fragmentación con pings grandes:**
```bash
# Ping normal (sin fragmentación)
ping fd11:22:33:0:0:0:0:1

# Ping con payload grande (forzará fragmentación 6LoWPAN)
ping fd11:22:33:0:0:0:0:1 size 200

# Ping aún más grande
ping fd11:22:33:0:0:0:0:1 size 500
```

**Observar en logs:**
- Busca mensajes de "Fragment" o "Reassembly" en los logs
- Nota el MTU efectivo de 6LoWPAN (~1280 bytes IPv6, pero fragmentado en capas inferiores)
- Mide latencia adicional por fragmentación

**Análisis de fragmentación:**
- Compara tiempos de respuesta entre pings pequeños y grandes
- Documenta el tamaño máximo sin fragmentación
- Observa comportamiento con múltiples saltos en la mesh

### 8. Evaluación de Resiliencia y Re-attach

**Simular falla del líder:**
1. Identifica cuál dispositivo es el líder (`state` command)
2. Apaga el dispositivo líder (desconecta USB)
3. Observa en el dispositivo restante:
   ```bash
   # Ver cambio de estado
   state

   # Ver logs de re-attach
   # (logs automáticos mostrarán MLE messages)
   ```

**Medir tiempos de convergencia:**
- Registra timestamp cuando se apaga el líder
- Registra cuando el nuevo líder es elegido (`state` cambia)
- Calcula tiempo de convergencia

**Pruebas adicionales de resiliencia:**
```bash
# Ver mensajes MLE (Mesh Link Establishment)
mle

# Forzar cambio de rol (si es router)
# (reiniciar dispositivo y observar re-attach)

# Probar con 3+ dispositivos para ver mesh routing
router table
neighbor table
```

**Análisis de resiliencia:**
- Documenta secuencia de eventos durante re-attach
- Mide tiempos de convergencia para diferentes tamaños de red
- Observa cómo se mantienen las direcciones IPv6 durante cambios

### 9. Análisis de Routing en Thread

**Comandos para análisis de routing:**
```bash
# Ver tabla de routers
router table

# Ver tabla de vecinos
neighbor table

# Ver rutas activas
routes

# Ver topología de red
neighbor table
```

**Experimentos de routing:**
1. **Routing directo:** Ping entre dispositivos conectados directamente
2. **Routing mesh:** Ping entre dispositivos con intermediarios
3. **Routing con falla:** Repetir después de simular falla

**Análisis:**
- Documenta cómo se construye la topología mesh
- Observa cambios en tablas de routing durante resiliencia
- Compara eficiencia de routing directo vs mesh

## Entregables
- Tabla de direcciones IPv6 clasificadas por tipo
- Logs de fragmentación con análisis de overhead
- Medidas de tiempos de convergencia para re-attach
- Diagramas de topología de red Thread con roles
- Análisis comparativo de rendimiento con/sin fragmentación