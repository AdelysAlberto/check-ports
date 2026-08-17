"""
Main Window Module
Ventana principal de la aplicación PySide6 con Splitter de 2 columnas (Lista y Detalle).
"""

import os
import sys
import platform
import subprocess

try:
    from PyQt5.QtWidgets import (
        QMainWindow, QWidget, QHBoxLayout, QSplitter, QVBoxLayout,
        QPushButton, QLabel, QStatusBar, QMessageBox
    )
    from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal as Signal
except ImportError:
    from PySide6.QtWidgets import (
        QMainWindow, QWidget, QHBoxLayout, QSplitter, QVBoxLayout,
        QPushButton, QLabel, QStatusBar, QMessageBox
    )
    from PySide6.QtCore import Qt, QTimer, QThread, Signal

from src.ui.port_list_widget import PortListWidget
from src.ui.port_detail_widget import PortDetailWidget
from src.core.scanner import scan_active_ports
from src.core.knowledge_base import KnowledgeBase
from src.core.updater import check_for_updates, perform_update
from src.version import __version__


class UpdateCheckWorker(QThread):
    """Hilo de fondo para comprobar actualizaciones sin bloquear la UI."""
    update_available = Signal(str)

    def run(self):
        res = check_for_updates()
        if res.is_ok() and res.value:
            self.update_available.emit(res.value)


class MainWindow(QMainWindow):
    """Ventana principal de CheckPorts."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"🛡️ CheckPorts — Inspector & Guard (v{__version__})")
        self.resize(1120, 680)

        self._new_version_tag = None
        self.kb_engine = KnowledgeBase()
        self.kb_engine.load()

        self._init_ui()

        # Timer para auto-refresco opcional (cada 5 segundos)
        self.timer = QTimer(self)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.refresh_ports)
        self.timer.start()

        # Primer escaneo al iniciar
        self.refresh_ports()

        # Comprobar actualizaciones en segundo plano
        self._check_updates_async()

    def _init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Barra de herramientas superior
        top_bar = QHBoxLayout()
        app_title = QLabel(f"🛡️ CheckPorts <span style='font-size: 12px; color: #94a3b8;'>v{__version__}</span>")
        app_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #38bdf8;")
        top_bar.addWidget(app_title)

        top_bar.addStretch()

        # Botón de Actualización Disponible (inicialmente oculto)
        self.btn_update = QPushButton("🚀 Actualizar")
        self.btn_update.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: #ffffff;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                padding: 6px 14px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        self.btn_update.clicked.connect(self._on_update_clicked)
        self.btn_update.hide()
        top_bar.addWidget(self.btn_update)

        # Botón de Privilegios / Sudo (si no está corriendo como root)
        is_root = os.geteuid() == 0 if hasattr(os, "geteuid") else False
        if not is_root:
            self.btn_sudo = QPushButton("⚡ Ejecutar como Administrador (Sudo)")
            self.btn_sudo.setStyleSheet("""
                QPushButton {
                    background-color: #f59e0b;
                    color: #0f172a;
                    font-weight: bold;
                    border: none;
                    border-radius: 6px;
                    padding: 6px 14px;
                }
                QPushButton:hover {
                    background-color: #d97706;
                    color: #ffffff;
                }
            """)
            self.btn_sudo.clicked.connect(self._elevate_privileges)
            top_bar.addWidget(self.btn_sudo)
        else:
            lbl_elevated = QLabel("🛡️ Superusuario")
            lbl_elevated.setStyleSheet("color: #10b981; font-weight: bold; font-size: 12px; margin-right: 8px;")
            top_bar.addWidget(lbl_elevated)

        self.btn_refresh = QPushButton("🔄 Refrescar")
        self.btn_refresh.setObjectName("btnRefresh")
        self.btn_refresh.clicked.connect(self.refresh_ports)
        top_bar.addWidget(self.btn_refresh)

        main_layout.addLayout(top_bar)

        # Splitter de 2 Columnas
        self.splitter = QSplitter(Qt.Horizontal)

        # Columna Izquierda (35%)
        self.list_widget = PortListWidget()
        self.list_widget.port_selected.connect(self._on_port_selected)
        self.splitter.addWidget(self.list_widget)

        # Columna Derecha (65%)
        self.detail_widget = PortDetailWidget()
        self.detail_widget.process_killed.connect(self.refresh_ports)
        self.splitter.addWidget(self.detail_widget)

        self.splitter.setSizes([380, 740])
        main_layout.addWidget(self.splitter)

        # Barra de Estado (Footer)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(f"Listo. CheckPorts v{__version__}")

    def _check_updates_async(self):
        """Inicia el worker en segundo plano para verificar releases."""
        self.update_worker = UpdateCheckWorker()
        self.update_worker.update_available.connect(self._on_update_detected)
        self.update_worker.start()

    def _on_update_detected(self, new_tag: str):
        """Muestra el botón de actualización cuando hay una versión superior."""
        self._new_version_tag = new_tag
        self.btn_update.setText(f"🚀 Actualizar a {new_tag}")
        self.btn_update.show()
        self.status_bar.showMessage(f"💡 ¡Nueva versión {new_tag} disponible! Haz clic en Actualizar.")

    def _on_update_clicked(self):
        """Ejecuta la actualización automática y avisa al usuario."""
        confirm = QMessageBox.question(
            self,
            "Actualizar CheckPorts",
            f"¿Deseas actualizar CheckPorts a la versión {self._new_version_tag or 'más reciente'} ahora?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return

        self.status_bar.showMessage("⬇️ Descargando e instalando actualización...")
        res = perform_update()
        if res.is_ok():
            QMessageBox.information(
                self,
                "Actualización Exitosa",
                "CheckPorts se actualizó correctamente. Por favor reinicia la aplicación para aplicar todos los cambios."
            )
            self.btn_update.hide()
            self.status_bar.showMessage("✅ Actualización completada. Reinicia la app.")
        else:
            QMessageBox.warning(
                self,
                "Error al Actualizar",
                f"No se pudo completar la actualización automática: {res.error}"
            )
            self.status_bar.showMessage("❌ Falló la actualización automática.")

    def _elevate_privileges(self):
        """Reinicia la aplicación solicitando privilegios de administrador de forma nativa."""
        is_macos = platform.system() == "Darwin"
        python_bin = sys.executable
        script_path = os.path.abspath(sys.argv[0])

        if is_macos:
            osa_script = (
                f'do shell script "\\"{python_bin}\\" \\"{script_path}\\" > /dev/null 2>&1 &" '
                f'with administrator privileges'
            )
            cmd = ["osascript", "-e", osa_script]
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    sys.exit(0)
                else:
                    err_msg = result.stderr.strip()
                    if "User cancelled" in err_msg or "-128" in err_msg:
                        self.status_bar.showMessage("ℹ️ Elevación de privilegios cancelada por el usuario.")
                    else:
                        QMessageBox.warning(self, "Elevación Cancelada", f"No se concedieron privilegios: {err_msg}")
            except Exception as e:
                QMessageBox.warning(self, "Error de Elevación", f"No se pudo solicitar elevación: {str(e)}")
        else:
            try:
                result = subprocess.run(["pkexec", python_bin, script_path], capture_output=True, text=True)
                if result.returncode == 0:
                    sys.exit(0)
                else:
                    self.status_bar.showMessage("ℹ️ Elevación cancelada.")
            except Exception as e:
                QMessageBox.warning(self, "Error de Elevación", f"No se pudo elevar privilegios: {str(e)}")

    def refresh_ports(self):
        """Escanea los puertos del sistema y actualiza ambas columnas."""
        scan_res = scan_active_ports()
        if scan_res.is_fail():
            self.status_bar.showMessage(f"⚠️ {scan_res.error}")
            QMessageBox.warning(self, "Error de Escaneo", scan_res.error)
            return

        raw_ports = scan_res.value
        enriched_ports = self.kb_engine.enrich_all(raw_ports)

        self.list_widget.update_ports(enriched_ports)
        self.status_bar.showMessage(f"✅ Escaneo completado. {len(enriched_ports)} puertos activos detectados.")

    def _on_port_selected(self, port_info):
        """Maneja la selección de un puerto en la lista de la izquierda."""
        self.detail_widget.display_port(port_info)


