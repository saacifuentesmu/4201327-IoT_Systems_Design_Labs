# Configuración del Entorno - Curso de IoT con ESP32‑C6

Esta guía te llevará paso a paso para configurar el entorno completo de desarrollo necesario para el curso usando Windows nativo y las herramientas gráficas de VS Code con la extensión ESP-IDF. La configuración se divide en tres partes principales:

1. **Prerrequisitos** - Instalación de Python y Git en Windows
2. **IDE y ESP-IDF** - Instalación de VS Code, extensión ESP-IDF e instalación del framework
3. **Workspace setup** - Configuración del workspace basado en este repositorio

---

## Parte 1: Prerrequisitos en Windows

### 1.1) Instalar Python 3.8 o superior

Descarga e instala Python desde [python.org](https://www.python.org/downloads/). Asegúrate de marcar la opción "Add Python to PATH" durante la instalación.

Verifica la instalación:
```cmd
python --version
pip --version
```

### 1.2) Instalar Git

Descarga e instala Git desde [git-scm.com](https://git-scm.com/download/win).

Verifica la instalación:
```cmd
git --version
```

## Parte 2: IDE y ESP-IDF

### 2.1) Instalar y configurar VS Code

1. Instalar [VS Code](https://code.visualstudio.com/download).
2. Instalar la extensión [ESP-IDF](https://marketplace.visualstudio.com/items?itemName=espressif.esp-idf-extension) desde el marketplace de VS Code.

### 2.2) Instalar ESP-IDF a través de la extensión

La extensión ESP-IDF puede instalar y configurar ESP-IDF automáticamente:

1. Abre VS Code.
2. Presiona `Ctrl+Shift+P` para abrir la paleta de comandos.
3. Busca y ejecuta `ESP-IDF: Install ESP-IDF`.
4. Selecciona la versión v5.1.
5. Elige la ubicación de instalación (por defecto está bien).
6. Espera a que se complete la instalación.

### 2.3) Configurar la extensión ESP-IDF

1. En VS Code, ejecuta `ESP-IDF: Configure ESP-IDF extension`.
2. Selecciona la instalación de ESP-IDF que acabas de instalar.
3. Elige `esp32c6` como target por defecto.

---

## Parte 3: Workspace Setup basado en este repositorio

### 3.1) Crear un fork del repositorio

Para tener tu propia copia del repositorio donde puedas guardar tus cambios y entregas:

1. Ve al repositorio original: [https://github.com/saacifuentesmu/4201327-IoT_Systems_Design_Labs](https://github.com/saacifuentesmu/4201327-IoT_Systems_Design_Labs)
2. Haz clic en el botón **"Fork"** en la esquina superior derecha
3. Selecciona tu cuenta de GitHub como destino del fork
4. Espera a que se complete el fork

### 3.2) Clonar tu fork

```cmd
# Clonar tu fork (elige una ubicación conveniente, ej. Documents)
cd %USERPROFILE%\Documents
git clone https://github.com/TU_USUARIO/4201327-IoT_Systems_Design_Labs.git
cd 4201327-IoT_Systems_Design_Labs
```

> **Nota:** Reemplaza `TU_USUARIO` con tu nombre de usuario de GitHub.

### 3.3) Verificar configuración

```cmd
# Probar build del proyecto base
cd lab_base
idf.py set-target esp32c6
idf.py build
```


---
---

## Inicio Rápido GUI con Extensión ESP-IDF

Para cada laboratorio, puedes usar la interfaz gráfica de la extensión ESP-IDF de VS Code en lugar de comandos de terminal. Esto simplifica el proceso y permite enfocarte en los conceptos de IoT:

1. Abrir VS Code → **Paleta de Comandos** (`Ctrl+Shift+P`) → **ESP‑IDF: Mostrar Ejemplos** → seleccionar el ejemplo apropiado (ver instrucciones del laboratorio para el ejemplo específico, ej. `esp-idf/examples/openthread/ot_cli`)
2. **ESP‑IDF: Establecer Objetivo** → `esp32c6`
3. **Editor de Configuración SDK de ESP-IDF** (GUI) para ajustar configuraciones específicas del laboratorio cuando se indique en los pasos.
4. Usar **Construir Proyecto ESP-IDF**, **Flashear Dispositivo** y **Monitorear Dispositivo** desde la barra de herramientas de la extensión.

_Tip:_ Los comandos de terminal se mantienen como alternativas en cada laboratorio; la GUI refleja las mismas acciones y es más intuitiva para principiantes.

---

## Configuración Completa ✅

Una vez completados todos los pasos, tendrás:
- ✅ Python 3.8+ instalado
- ✅ Git instalado
- ✅ ESP-IDF v5.1 instalado y configurado
- ✅ Repositorio del curso clonado
- ✅ VS Code con extensión ESP-IDF
- ✅ Drivers USB configurados (si necesario)

## Workflow diario

Para trabajar en el curso cada día:

```cmd
# 1. Conectar la ESP32-C6 al puerto USB
# (Los drivers se instalan automáticamente o manualmente como en Parte 2.4)

# 2. Abrir VS Code en el directorio de tu fork
code %USERPROFILE%\Documents\4201327-IoT_Systems_Design_Labs

# 3. Trabajar con los laboratorios usando la GUI de la extensión ESP-IDF
# ... seguir instrucciones del laboratorio correspondiente
```

---

## Smoke Test: Thread CLI + CoAP (Validación Rápida)

Antes del primer laboratorio formal, realiza esta prueba mínima para confirmar que la pila OpenThread y CoAP funcionan en tu entorno usando la GUI de VS Code.

### 1) Compilar y flashear el proyecto base (`lab_base`)

1. Abre VS Code en el directorio de tu fork `4201327-IoT_Systems_Design_Labs`.
2. Abre la carpeta `lab_base`.
3. En la barra de herramientas ESP-IDF, haz clic en **ESP-IDF: Establecer Objetivo** y selecciona `esp32c6`.
4. Haz clic en **ESP-IDF: Construir Proyecto**.
5. Conecta la ESP32-C6 y haz clic en **ESP-IDF: Flashear Dispositivo**.
6. Haz clic en **ESP-IDF: Monitorear Dispositivo**.

En la consola (shell OpenThread):
```
ot dataset init new
ot dataset commit active
ot ifconfig up
ot thread start
state   # Debe mostrar: leader o child tras unos segundos
```

Apunta las direcciones IPv6:
```
ipaddr
```

### 2) Preparar segundo nodo (misma app base)
Conecta otra placa y repite los pasos de build/flash desde VS Code. Forma la red igual que el primer nodo. (Los endpoints CoAP se implementarán en el Lab 1; por ahora solo validamos Thread.)

### 3) (Opcional) Captura Rápida
Inicia tu sniffer 802.15.4 en el canal asignado y guarda un pcap de 30 s para usarlo en el Lab 2.

---

