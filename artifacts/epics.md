# Épicas e Historias de Usuario (Sprint Breakdown)
## System: Ubuntu Port Inspector

> *"Es una bendición... y una maldición. Cada épica está minuciosamente ordenada, etiquetada y libre de ambigüedades."* — **Adrian Monk**

---

## 🗂️ EP-01: Core System & Knowledge Base Engine
- **US-01.1: Base de Conocimientos JSON (`data/ports_knowledge.json`)**
  - Crear el archivo JSON con la información detallada de más de 100 puertos estándar de Linux y desarrollo web.
- **US-01.2: Scanner de Sockets y Procesos (`src/core/scanner.py`)**
  - Implementar la función `scan_active_ports()` usando `psutil.net_connections()`.
- **US-01.3: Gestor de Procesos Linux (`src/core/process_manager.py`)**
  - Implementar el envío de señales `SIGTERM` / `SIGKILL` con validación de PIDs protegidos del sistema.

---

## 🎨 EP-02: Interfaz Nativa de Escritorio (PySide6)
- **US-02.1: Ventana Principal & Tema QSS (`src/ui/main_window.py`, `src/ui/styles.py`)**
  - Configurar `QMainWindow` con layout horizontal dividida en 2 columnas y aplicar el tema QSS Dark Mode.
- **US-02.2: Columna Izquierda - Lista de Puertos (`src/ui/port_list_widget.py`)**
  - Implementar `QTreeWidget` clasificado en "Puertos Comunes de Ubuntu" y "Puertos No Comunes / Apps" con filtro de búsqueda.
- **US-02.3: Columna Derecha - Panel de Detalle & Acciones (`src/ui/port_detail_widget.py`)**
  - Renderizado de información extendida del proceso seleccionado, tarjeta de descripción de la base de conocimientos y botones de acción (Matar proceso, copiar datos).
