# Arquitectura Visual & Sistema de Estilos QSS (PySide6)
## Ubuntu Port Guard & Inspector

> *"¿Estilos por defecto del sistema sin personalizar? Qué decepción tan absoluta. La interfaz tendrá una paleta impecable, un contraste perfecto y una elegancia insuperable. Es todo."* — **Miranda Priestly**

---

## 🎨 1. Palette & Design Tokens (QSS Theme Constants)

```ini
; Main Backgrounds & Surfaces
@bg_window          = #0f172a (Slate 900 - Fondo Principal)
@bg_card            = #1e293b (Slate 800 - Tarjetas y Contenedores)
@bg_sidebar         = #1e293b (Slate 800 - Lista de Puertos)
@bg_input           = #334155 (Slate 700 - Campos de Búsqueda)

; Accent & Status Colors
@color_primary      = #3b82f6 (Blue 500 - Elementos Activos / Selección)
@color_accent       = #6366f1 (Indigo 500 - Destacados)
@color_system_port  = #10b981 (Emerald 500 - Puertos Comunes Ubuntu)
@color_custom_port  = #f59e0b (Amber 500 - Puertos No Comunes / Apps)
@color_danger       = #ef4444 (Red 500 - Botón Matar Proceso / SIGKILL)
@color_danger_hover = #dc2626 (Red 600)

; Text & Typography
@text_primary       = #f8fafc (Slate 50 - Texto Principal)
@text_secondary     = #94a3b8 (Slate 400 - Etiquetas y Subtítulos)
@text_muted         = #64748b (Slate 500 - Texto Deshabilitado/Footers)
@font_family        = 'Ubuntu', 'Inter', 'DejaVu Sans', sans-serif
@font_mono          = 'Ubuntu Mono', 'JetBrains Mono', monospace
```

---

## 💅 2. QSS Style Sheet Master Document (`src/styles/theme.qss`)

```css
/* Base Application Window */
QMainWindow, QDialog {
    background-color: #0f172a;
    color: #f8fafc;
    font-family: 'Ubuntu', 'Inter', sans-serif;
    font-size: 13px;
}

/* Master-Detail Frame Panels */
QFrame#masterPanel, QFrame#detailPanel {
    background-color: #1e293b;
    border-radius: 8px;
    border: 1px solid #334155;
}

/* Header & Search Bar */
QLineEdit#searchBox {
    background-color: #334155;
    color: #f8fafc;
    border: 1px solid #475569;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 13px;
}
QLineEdit#searchBox:focus {
    border: 1px solid #3b82f6;
}

/* Tree & List Items (Ports Column) */
QTreeWidget, QListWidget {
    background-color: #1e293b;
    color: #f8fafc;
    border: none;
    outline: none;
}

QTreeWidget::item, QListWidget::item {
    padding: 8px;
    border-radius: 4px;
    margin-bottom: 2px;
}

QTreeWidget::item:selected, QListWidget::item:selected {
    background-color: #3b82f6;
    color: #ffffff;
    font-weight: bold;
}

QTreeWidget::item:hover:!selected, QListWidget::item:hover:!selected {
    background-color: #334155;
}

/* Badges for Common vs Non-Common Ports */
QLabel.badgeSystem {
    background-color: #064e3b;
    color: #34d399;
    border-radius: 4px;
    padding: 2px 6px;
    font-size: 11px;
    font-weight: bold;
}

QLabel.badgeCustom {
    background-color: #78350f;
    color: #fbbf24;
    border-radius: 4px;
    padding: 2px 6px;
    font-size: 11px;
    font-weight: bold;
}

/* Action Buttons */
QPushButton {
    background-color: #334155;
    color: #f8fafc;
    border: 1px solid #475569;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 600;
}
QPushButton:hover {
    background-color: #475569;
}

QPushButton#btnKill {
    background-color: #ef4444;
    color: #ffffff;
    border: none;
}
QPushButton#btnKill:hover {
    background-color: #dc2626;
}

/* Detail Code / Monospace Boxes */
QTextEdit#codeBlock, QLabel.monoText {
    font-family: 'Ubuntu Mono', monospace;
    background-color: #0f172a;
    color: #38bdf8;
    border-radius: 4px;
    padding: 6px;
}
```
