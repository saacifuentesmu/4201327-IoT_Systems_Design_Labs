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
3. Busca y ejecuta `ESP-IDF: Configure ESP-IDF Extension`.
4. Selecciona "Express", luego la versión v5.5.1.
5. Elige la ubicación de instalación (por defecto está bien).
6. Presiona el botón "Install" y espera a que se complete la instalación.
7. Elige `esp32c6` como target por defecto.

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
git clone https://github.com/<TU_USUARIO>/4201327-IoT_Systems_Design_Labs.git
cd 4201327-IoT_Systems_Design_Labs
```

> **Nota:** Reemplaza `<TU_USUARIO>` con tu nombre de usuario de GitHub.

---
---

## Inicio Rápido con Extensión ESP-IDF

Para cada laboratorio, puedes usar la interfaz gráfica de la extensión ESP-IDF de VS Code:

1. Abrir VS Code → **Paleta de Comandos** (`Ctrl+Shift+P`) → **ESP‑IDF: Mostrar Ejemplos** → seleccionar el ejemplo apropiado (ver instrucciones del laboratorio para el ejemplo específico, ej. `esp-idf/examples/openthread/ot_cli`)
2. **ESP‑IDF: Establecer Objetivo** → `esp32c6`
3. **Editor de Configuración SDK de ESP-IDF** (GUI) para ajustar configuraciones específicas del laboratorio cuando se indique en los pasos.
4. Usar **Construir Proyecto ESP-IDF**, **Flashear Dispositivo** y **Monitorear Dispositivo** desde la barra de herramientas del IDE.

---

## Configuración Completa ✅

Una vez completados todos los pasos, tendrás:
- ✅ Python 3.8+ instalado
- ✅ Git instalado
- ✅ ESP-IDF v5.5.1 instalado y configurado
- ✅ Repositorio del curso clonado
- ✅ VS Code con extensión ESP-IDF

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

Antes del primer laboratorio formal, realiza esta prueba mínima para confirmar que el ejemplo de OpenThread funciona en tu entorno usando la GUI de VS Code.

### Compilar y flashear el proyecto base (`lab_base`)

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


---

