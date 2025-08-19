# Configuración del Entorno - Curso de IoT con ESP32‑C6

Esta guía te llevará paso a paso para configurar el entorno completo de desarrollo necesario para el curso. La configuración se divide en tres partes principales:

1. **WSL2 (Ubuntu)** - Preparación del entorno Linux en Windows
2. **Python, pip y west** - Instalación de herramientas de desarrollo
3. **Workspace setup** - Configuración del workspace Zephyr basado en este repositorio
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

## Parte 2: Python, pip y west (en WSL2)

Una vez dentro de WSL2 Ubuntu, configurar las herramientas de desarrollo de Python.

### 2.1) Actualizar sistema e instalar dependencias

```bash
# Actualizar Ubuntu
sudo apt update && sudo apt upgrade -y

# Instalar dependencias básicas para Zephyr
sudo apt install --no-install-recommends git cmake ninja-build gperf ccache \
  dfu-util device-tree-compiler wget python3-pip python3-dev python3-venv \
  xz-utils file make gcc gcc-multilib g++-multilib libsdl2-dev libmagic1

# add user to the dialout group for later USB access
sudo usermod -a -G dialout $USER

```

### 2.2) Crear y activar entorno virtual de Python

```bash
# Crear directorio y entorno virtual para el workspace
python3 -m venv ~/zephyrproject/.venv

# Activar entorno virtual
source ~/zephyrproject/.venv/bin/activate
```

> ⚠️ **Importante**: Siempre activa el entorno virtual (`source ~/zephyrproject/.venv/bin/activate`) antes de usar `west` o herramientas de Zephyr.

### 2.3) Instalar west

```bash
# Con el venv activado, instalar west
pip install west
```

---

## Parte 3: Workspace Setup basado en este repositorio (manifest)

### 3.1) Inicializar workspace Zephyr desde el manifiesto de este repo

```bash
# Asegúrate de estar en el directorio correcto con venv activado
cd ~/zephyrproject
source .venv/bin/activate

# Inicializar el workspace apuntando a este repo como manifiesto
west init -m https://github.com/saacifuentesmu/4201327-IoT_Systems_Design_Labs ~/zephyrproject

# Entrar al workspace y sincronizar proyectos (Zephyr y módulos)
cd ~/zephyrproject
west update

# Exportar el paquete CMake de Zephyr
west zephyr-export

# Instalar dependencias adicionales de Python de los paquetes
west packages pip --install

```

### 3.2) Instalar Zephyr SDK

```bash
# Instalar solo el toolchain necesario para ESP32-C6 (RISC-V)
cd ~/zephyrproject/zephyr
west blobs fetch hal_espressif
west sdk install --toolchains riscv64-zephyr-elf

```

### 3.3) Verificar configuración

```bash
# Probar build de ejemplo básico (Hello World)
cd ~/zephyrproject/zephyr
west build -p auto -b esp32c6_devkitc/esp32c6/hpcore samples/hello_world

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

# 2. En WSL, activar entorno (venv) cada sesión
cd ~/zephyrproject
source .venv/bin/activate

# 3. Trabajar con los laboratorios
cd 4100901-IoT_Course
# ... seguir instrucciones del laboratorio correspondiente
```
