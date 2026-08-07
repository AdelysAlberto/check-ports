"""
Port List Widget Module (Columna Izquierda)
Muestra la lista de puertos categorizados en "Puertos Comunes de Ubuntu" y "Puertos No Comunes / Apps"
con barra de búsqueda en tiempo real.
"""

try:
    from PyQt5.QtWidgets import (
        QWidget, QVBoxLayout, QLineEdit, QTreeWidget, QTreeWidgetItem, QLabel, QHBoxLayout
    )
    from PyQt5.QtCore import pyqtSignal as Signal, Qt
    from PyQt5.QtGui import QIcon, QColor, QFont
except ImportError:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QLineEdit, QTreeWidget, QTreeWidgetItem, QLabel, QHBoxLayout
    )
    from PySide6.QtCore import Signal, Qt
    from PySide6.QtGui import QIcon, QColor, QFont
from typing import List
from src.models.port_model import PortInfo


class PortListWidget(QWidget):
    """Widget de la columna izquierda con la lista clasificada de puertos."""

    # Señal emitida al seleccionar un puerto (PortInfo)
    port_selected = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._all_ports: List[PortInfo] = []
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)

        # Encabezado
        header_layout = QHBoxLayout()
        title = QLabel("📡 Puertos Usados")
        title.setObjectName("sectionTitle")
        header_layout.addWidget(title)
        layout.addLayout(header_layout)

        # Caja de búsqueda
        self.search_box = QLineEdit()
        self.search_box.setObjectName("searchBox")
        self.search_box.setPlaceholderText("🔍 Buscar por puerto, servicio o proceso...")
        self.search_box.textChanged.connect(self._filter_ports)
        layout.addWidget(self.search_box)

        # Árbol de puertos (QTreeWidget)
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setAnimated(True)
        self.tree.itemSelectionChanged.connect(self._on_item_selected)
        layout.addWidget(self.tree)

        # Contador de resumen en footer
        self.status_label = QLabel("Escaneando puertos...")
        self.status_label.setObjectName("subtitleLabel")
        layout.addWidget(self.status_label)

    def update_ports(self, ports: List[PortInfo]):
        """Actualiza la lista completa de puertos y renderiza el árbol."""
        self._all_ports = ports
        self._render_tree(ports)

    def _render_tree(self, ports: List[PortInfo]):
        """Renderiza los nodos de categorías y puertos."""
        self.tree.clear()

        # Categoría 1: Puertos Comunes de Ubuntu
        common_root = QTreeWidgetItem(["🟢 Puertos Comunes de Ubuntu (Sistema)"])
        font = QFont()
        font.setBold(True)
        common_root.setFont(0, font)

        # Categoría 2: Puertos No Comunes / Apps
        custom_root = QTreeWidgetItem(["🟠 Puertos No Comunes / Aplicaciones"])
        custom_root.setFont(0, font)

        common_count = 0
        custom_count = 0

        for p in ports:
            proc_name = p.process.name if p.process else "Sin PID"
            item_text = f"[{p.protocol} {p.port}]  {p.service_name}  ({proc_name})"
            item = QTreeWidgetItem([item_text])
            item.setData(0, Qt.UserRole, p)

            if p.is_common:
                common_root.addChild(item)
                common_count += 1
            else:
                custom_root.addChild(item)
                custom_count += 1

        self.tree.addTopLevelItem(common_root)
        self.tree.addTopLevelItem(custom_root)

        common_root.setExpanded(True)
        custom_root.setExpanded(True)

        self.status_label.setText(f"Total: {len(ports)} puertos | 🟢 Sistema: {common_count} | 🟠 Apps: {custom_count}")

    def _filter_ports(self, text: str):
        """Filtra la lista de puertos por texto ingresado."""
        query = text.lower().strip()
        if not query:
            self._render_tree(self._all_ports)
            return

        filtered = [
            p for p in self._all_ports
            if query in str(p.port) or
               query in p.service_name.lower() or
               query in p.protocol.lower() or
               (p.process and (query in p.process.name.lower() or query in p.process.cmdline.lower()))
        ]
        self._render_tree(filtered)

    def _on_item_selected(self):
        """Dispara la señal con el objeto PortInfo seleccionado."""
        selected_items = self.tree.selectedItems()
        if not selected_items:
            return

        item = selected_items[0]
        port_info = item.data(0, Qt.UserRole)
        if port_info:
            self.port_selected.emit(port_info)
