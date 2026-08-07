"""
QSS Styles Module
Módulo de carga y aplicación de temas CSS/QSS para PySide6 nativo en Ubuntu.
"""

DARK_THEME_QSS = """
/* Base Window & Dialogs */
QMainWindow, QDialog, QMessageBox {
    background-color: #1e293b;
    color: #ffffff;
    font-family: 'Ubuntu', 'Inter', sans-serif;
    font-size: 13px;
}

QMessageBox QLabel, QDialog QLabel {
    color: #ffffff !important;
    font-size: 13px;
    font-weight: 500;
    background-color: transparent;
}

QMessageBox QPushButton, QDialog QPushButton {
    background-color: #334155;
    color: #ffffff !important;
    border: 1px solid #475569;
    border-radius: 6px;
    padding: 6px 16px;
    min-width: 75px;
    font-weight: bold;
}

QMessageBox QPushButton:hover, QDialog QPushButton:hover {
    background-color: #3b82f6;
    color: #ffffff !important;
}

/* Master-Detail Splitter & Panels */
QSplitter::handle {
    background-color: #334155;
    width: 2px;
}

QFrame#cardFrame {
    background-color: #1e293b;
    border-radius: 8px;
    border: 1px solid #334155;
}

/* Header & Inputs */
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

/* Tree & List Views (Left Column) */
QTreeWidget {
    background-color: #1e293b;
    color: #f8fafc;
    border: 1px solid #334155;
    border-radius: 8px;
    outline: none;
    padding: 4px;
}

QTreeWidget::item {
    padding: 6px 8px;
    border-radius: 4px;
    margin-bottom: 2px;
}

QTreeWidget::item:selected {
    background-color: #3b82f6;
    color: #ffffff;
    font-weight: bold;
}

QTreeWidget::item:hover:!selected {
    background-color: #334155;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: #0f172a;
    width: 8px;
    margin: 0px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #475569;
    min-height: 20px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #64748b;
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

QPushButton:pressed {
    background-color: #1e293b;
}

QPushButton:disabled {
    background-color: #1e293b;
    color: #64748b;
    border: 1px solid #334155;
}

QPushButton#btnRefresh {
    background-color: #2563eb;
    color: #ffffff;
    border: none;
}

QPushButton#btnRefresh:hover {
    background-color: #1d4ed8;
}

QPushButton#btnKill {
    background-color: #dc2626;
    color: #ffffff;
    border: none;
}

QPushButton#btnKill:hover {
    background-color: #b91c1c;
}

QPushButton#btnCopy {
    background-color: #475569;
    color: #ffffff;
    border: none;
}

QPushButton#btnCopy:hover {
    background-color: #64748b;
}

/* Labels & Status */
QLabel#sectionTitle {
    font-size: 16px;
    font-weight: bold;
    color: #38bdf8;
}

QLabel#subtitleLabel {
    font-size: 12px;
    color: #94a3b8;
}

QLabel#detailLabel {
    font-size: 13px;
    color: #f8fafc;
}

QLabel#keyLabel {
    font-size: 12px;
    font-weight: bold;
    color: #94a3b8;
}

QTextEdit#descBox {
    background-color: #0f172a;
    color: #e2e8f0;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 8px;
    font-size: 12px;
}
"""


def apply_theme(app):
    """Aplica el tema visual QSS a la aplicación QApplication."""
    app.setStyleSheet(DARK_THEME_QSS)
