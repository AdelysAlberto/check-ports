# 🛡️ CheckPorts — Inspector & Guard (Ubuntu & macOS)

> **Aplicación Open Source** de escritorio nativa para el monitoreo, clasificación, auditoría y gestión de puertos de red abiertos y procesos vinculados en tiempo real.

![Open Source](https://img.shields.io/badge/License-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-green.svg)
![Platform](https://img.shields.io/badge/Platform-Ubuntu%20%7C%20macOS-orange.svg)

---

## 👨‍💻 Desarrollador & Créditos

- **Nombre**: Adelys Alberto Belén
- **GitHub**: [@adelysalberto](https://github.com/adelysalberto)
- **LinkedIn**: [https://www.linkedin.com/in/adelysalberto](https://www.linkedin.com/in/adelysalberto)
- **Licencia**: Open Source (Licencia MIT)

---

## 🚀 Características Principales

- 📊 **Distribución en 2 Columnas (Master-Detail)**:
  - **Columna Izquierda**: Árbol clasificado de puertos activos divididos en **Puertos Comunes del Sistema** (SSH 22, DNS 53, HTTP 80, HTTPS 443, CUPS 631, mDNS 5353, etc.) y **Puertos No Comunes / Aplicaciones** (Node.js 3000, Vite 5173, PostgreSQL 5432, Redis 6379, etc.).
  - **Columna Derecha**: Panel extendido con el detalle completo del proceso (PID, Nombre, Usuario, Ruta de ejecutable, Línea de comandos con argumentos, consumo de CPU y RAM) y tarjetas de conocimiento.
- 🔍 **Buscador en Tiempo Real**: Filtrado dinámico instantáneo por número de puerto, protocolo (TCP/UDP), nombre de servicio o binario ejecutable.
- 📚 **Base de Conocimiento Local Integrada (`data/ports_knowledge.json`)**:
  - Consulta en tiempo constante $O(1)$ en memoria.
  - Explicación en español del propósito del puerto, nivel de riesgo y recomendaciones de seguridad.
- 🛑 **Control Seguro de Procesos**:
  - Botón de terminación de procesos (**SIGKILL** / **SIGTERM**) previa confirmación explícita mediante un cuadro modal nítido y de alto contraste.
  - **Escudo de Procesos Protegidos**: Deshabilita automáticamente la opción de finalizar PIDs críticos del sistema (`systemd`, `init`, `dbus-daemon`, `gnome-shell`, `launchd`, `kernel_task`, `WindowServer`, etc.) y despliega un banner de advertencia explicativo.
- 📋 **Acciones Rápidas**: Copiado en un clic de los detalles del puerto/proceso al portapapeles.
- 💻 **Compatibilidad Multiplataforma**: Diseñada para **Ubuntu Linux** (Wayland / X11) y **macOS**.

---

<img width="1110" height="711" alt="image" src="https://github.com/user-attachments/assets/6e25140a-b0f4-4cd3-b9f9-175ebbe0046c" />


## 🏗️ Estructura del Proyecto

```text
check-ports/
├── main.py                     # Punto de entrada principal (QApplication + MainWindow)
├── README.md                   # Documentación principal del proyecto y créditos Open Source
├── walkthrough.md              # Guía de implementación y pruebas realizadas
├── data/
│   └── ports_knowledge.json    # Catálogo local estructurado con +100 puertos
├── src/
│   ├── core/
│   │   ├── scanner.py          # Inspector de sockets y conexiones TCP/UDP (psutil + socket)
│   │   ├── knowledge_base.py   # Motor de enriquecimiento de información en memoria O(1)
│   │   └── process_manager.py  # Gestor de señales de terminación y protección de PIDs
│   ├── models/
│   │   └── port_model.py       # Modelos de datos PortInfo y ProcessDetail
│   ├── ui/
│   │   ├── main_window.py      # Ventana principal PySide6/PyQt5 con Splitter de 2 columnas
│   │   ├── port_list_widget.py # Columna izquierda: Árbol clasificado y barra de búsqueda
│   │   ├── port_detail_widget.py# Columna derecha: Detalle extendido, KB y diálogos modales
│   │   └── styles.py           # Sistema visual QSS Dark Mode (Slate & Neon Accent)
│   └── utils/
│       └── result.py           # Implementación del Result Pattern (Result[T, E])
└── artifacts/                  # Especificaciones del proyecto (Plan Maestro, PRD, UX, Arch, Security)
```

---

## 📦 Requisitos Previos

- **Python 3.10+**
- **Sistemas Operativos Soportados**:
  - Ubuntu 20.04 / 22.04 / 24.04+ (GNOME, Wayland o X11)
  - macOS Monterey / Ventura / Sonoma / Sequoia+

---

## ⚙️ Instalación y Uso

### 1. Clonar o Navegar al Directorio
```bash
git clone https://github.com/adelysalberto/check-ports.git
cd check-ports
```

### 2. Crear y Activar el Entorno Virtual (`.venv`)
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar las Dependencias
```bash
pip install PyQt5 psutil
```

### 4. Ejecutar la Aplicación
```bash
.venv/bin/python3 main.py
```

> 💡 **Nota de Permisos**: Para ver la totalidad de PIDs pertenecientes al usuario `root` u otros servicios de sistema en Linux/macOS, ejecuta la aplicación con privilegios elevados:
> ```bash
> sudo .venv/bin/python3 main.py
> ```

---

## 🔒 Seguridad y Privilegios

La aplicación implementa el patrón **Critical PID Shield** en `src/core/process_manager.py`:
- Se prohíbe explícitamente enviar señales de terminación a los PIDs `0` y `1`.
- Se bloquea la finalización de los siguientes daemon vitales del sistema:
  - **Linux**: `systemd`, `init`, `kthreadd`, `systemd-journald`, `systemd-logind`, `dbus-daemon`, `xorg`, `wayland`, `gnome-shell`.
  - **macOS**: `launchd`, `kernel_task`, `windowserver`, `syslogd`, `opendirectoryd`, `powerd`, `logd`.

---

## 📜 Licencia Open Source

Este proyecto es software libre de código abierto distribuido bajo la **Licencia MIT**. Desarrollado por **Adelys Alberto Belén** para la inspección y administración limpia de puertos y procesos en entornos de desarrollo y administración de sistemas Linux/macOS.
