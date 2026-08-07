"""
Main Window Module
Ventana principal de la aplicación PySide6 con Splitter de 2 columnas (Lista y Detalle).
"""

try:
    from PyQt5.QtWidgets import (
        QMainWindow, QWidget, QHBoxLayout, QSplitter, QVBoxLayout,
        QPushButton, QLabel, QStatusBar, QMessageBox
    )
    from PyQt5.QtCore import Qt, QTimer
except ImportError:
    from PySide6.QtWidgets import (
        QMainWindow, QWidget, QHBoxLayout, QSplitter, QVBoxLayout,
        QPushButton, QLabel, QStatusBar, QMessageBox
    )
    from PySide6.QtCore import Qt, QTimer
from src.ui.port_list_widget import PortListWidget
from src.ui.port_detail_widget import PortDetailWidget
from src.core.scanner import scan_active_ports
from src.core.knowledge_base import KnowledgeBase


class MainWindow(QMainWindow):
    """Ventana principal de CheckPorts."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🛡️ CheckPorts — Inspector & Guard")
        self.resize(1100, 680)

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

    def _init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Barra de herramientas superior
        top_bar = QHBoxLayout()
        app_title = QLabel("🛡️ CheckPorts — Inspector & Guard")
        app_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #38bdf8;")
        top_bar.addWidget(app_title)

        top_bar.addStretch()

        self.btn_refresh = QPushButton("🔄 Refrescar Puertos")
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

        self.splitter.setSizes([380, 720])
        main_layout.addWidget(self.splitter)

        # Barra de Estado (Footer)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Listo. Escaneando sistema Ubuntu...")

    def refresh_ports(self):
        """Escanea los puertos del sistema y actualiza ambas columnas."""
        scan_res = scan_active_ports()
        if scan_res.is_fail():
            self.status_bar.showMessage(f"⚠️ {scan_res.error}")
            QMessageBox.warning(self, "Error de Permisos", scan_res.error)
            return

        raw_ports = scan_res.value
        enriched_ports = self.kb_engine.enrich_all(raw_ports)

        self.list_widget.update_ports(enriched_ports)
        self.status_bar.showMessage(f"✅ Escaneo completado. {len(enriched_ports)} puertos activos detectados.")

    def _on_port_selected(self, port_info):
        """Maneja la selección de un puerto en la lista de la izquierda."""
        self.detail_widget.display_port(port_info)
