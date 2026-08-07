#!/usr/bin/env python3
"""
Ubuntu Port Guard & Inspector
Punto de entrada principal de la aplicación de escritorio nativa en Ubuntu (Wayland / X11).
"""

import sys
import os

# Asegurar que src esté en el path de módulos
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from PyQt5.QtWidgets import QApplication
except ImportError:
    from PySide6.QtWidgets import QApplication

from src.ui.main_window import MainWindow
from src.ui.styles import apply_theme


def main():
    app = QApplication(sys.argv)
    apply_theme(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_() if hasattr(app, 'exec_') else app.exec())


if __name__ == "__main__":
    main()
