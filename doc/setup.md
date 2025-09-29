# Configuración del Entorno - Curso de IoT con ESP32‑C6

Esta guía te llevará paso a paso para configurar el entorno completo de desarrollo necesario para el curso. La configuración se divide en tres partes principales:

1. **WSL2 (Ubuntu)** - Preparación del entorno Linux en Windows
2. **ESP-IDF** - Instalación del framework de desarrollo
3. **Workspace setup** - Configuración del workspace basado en este repositorio
4. **IDE setup** - Configuración de VS Code y USB

---

## Parte 1: WSL2 (Ubuntu) - Preparación del Entorno Windows

### Prerrequisitos
- Windows 11 (actualizado)
- Acceso de administrador
- Conectividad a Internet

### 1.1) Habilitar WSL2 e instalar Ubuntu

```powershell
# Habilitar características de WSL (PowerShell Admin)
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux

```

**Reiniciar el sistema**, luego instalar Ubuntu:

```powershell
# Instalar Ubuntu (PowerShell)
wsl --install Ubuntu

```

## Parte 2: ESP-IDF (en WSL2)

Una vez dentro de WSL2 Ubuntu, instalar ESP-IDF.

### 2.1) Actualizar sistema e instalar dependencias

```bash
# Actualizar Ubuntu
sudo apt update && sudo apt upgrade -y

# Instalar dependencias básicas para ESP-IDF
sudo apt install git wget flex bison gperf python3 python3-pip python3-venv cmake ninja-build ccache libffi-dev libssl-dev dfu-util libusb-1.0-0

# add user to the dialout group for later USB access
sudo usermod -a -G dialout $USER

```

### 2.2) Instalar ESP-IDF

```bash
# Clonar ESP-IDF
cd ~
git clone -b v5.1 --recursive https://github.com/espressif/esp-idf.git

# Instalar herramientas
cd esp-idf
./install.sh esp32c6

# Configurar entorno
. ./export.sh
```

> ⚠️ **Importante**: Siempre ejecuta `. ~/esp-idf/export.sh` en cada sesión antes de usar idf.py.

---

## Parte 3: Workspace Setup basado en este repositorio

### 3.1) Clonar el repositorio del curso

```bash
# Clonar el repositorio
cd ~
git clone https://github.com/saacifuentesmu/4201327-IoT_Systems_Design_Labs.git
cd 4201327-IoT_Systems_Design_Labs

```

### 3.2) Verificar configuración

```bash
# Probar build del proyecto base
cd lab_base
idf.py set-target esp32c6
idf.py build

```

---

## Parte 4: IDE Setup (VS Code)

### 4.1) Configurar VS Code

- Instalar [VS Code](https://code.visualstudio.com/download).
- Instalar [WSL Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl).

En VS Code, hacer clic en el ícono azul `><` (esquina inferior izquierda) y seleccionar "Connect to WSL".

### 4.2) Configurar USB passthrough

Para poder flashear la ESP32-C6 desde WSL, necesitas configurar USB passthrough:

```powershell
# Instalar usbipd-win (PowerShell como Admin)
winget install --id=dorssel.usbipd-win -e
```

**Configuración por dispositivo** (hacer una vez por ESP32-C6):
```powershell
# Listar dispositivos USB
usbipd list

# Vincular el dispositivo ESP32-C6 (reemplazar BUSID como <x-y>)
usbipd bind --busid <x-y>

# Conectar a WSL (hacer cada vez que conectes la placa)
usbipd attach --wsl --busid <x-y> --auto-attach
```

---

## Configuración Completa ✅

Una vez completados todos los pasos, tendrás:
- ✅ WSL2 Ubuntu funcionando
- ✅ Python virtual environment con west
- ✅ Repositorio del curso clonado
- ✅ Zephyr SDK instalado
- ✅ VS Code con Remote WSL
- ✅ USB passthrough configurado

## Workflow diario

Para trabajar en el curso cada día:

```bash
# 1. Conectar ESP32-C6 en Windows (PowerShell Admin)
usbipd attach --wsl --busid 3-2 --auto-attach

# 2. En WSL, activar entorno ESP-IDF cada sesión
cd ~/esp-idf
. ./export.sh

# 3. Trabajar con los laboratorios
cd ~/4201327-IoT_Systems_Design_Labs
# ... seguir instrucciones del laboratorio correspondiente
```

---

## Smoke Test: Thread CLI + CoAP (Validación Rápida)

Antes del primer laboratorio formal, realiza esta prueba mínima para confirmar que la pila OpenThread y CoAP funcionan en tu entorno.

### 1) Compilar y flashear el proyecto base (`lab_base`)
```bash
cd ~/4201327-IoT_Systems_Design_Labs/lab_base
idf.py set-target esp32c6
idf.py build
idf.py flash
idf.py monitor
```

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
Conecta otra placa y repite el build/flash:
```bash
idf.py build
idf.py flash
idf.py monitor
```
Forma la red igual que el primer nodo. (Los endpoints CoAP se implementarán en el Lab 1; por ahora solo validamos Thread.)

### 3) (Opcional) Captura Rápida
Inicia tu sniffer 802.15.4 en el canal asignado y guarda un pcap de 30 s para usarlo en el Lab 2.

---

