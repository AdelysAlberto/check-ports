"""
Port Detail Widget Module (Columna Derecha)
Muestra la información técnica extendida del puerto seleccionado, datos del proceso,
descripción de la base de conocimientos y botones de acción (Matar Proceso / Copiar Info).
"""

try:
    from PyQt5.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit,
        QFrame, QDialog, QApplication
    )
    from PyQt5.QtCore import pyqtSignal as Signal, Qt
except ImportError:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit,
        QFrame, QDialog, QApplication
    )
    from PySide6.QtCore import Signal, Qt
from typing import Optional
from src.models.port_model import PortInfo
from src.core.process_manager import terminate_process, can_terminate_process


class CustomDialog(QDialog):
    """Diálogo modal personalizado con diseño visual oscuro y texto claro garantizado."""
    def __init__(self, parent=None, title: str = "Mensaje", text: str = "", icon_symbol: str = "ℹ️", is_confirm: bool = False):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(450)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        content_layout = QHBoxLayout()
        icon_lbl = QLabel(icon_symbol)
        icon_lbl.setStyleSheet("font-size: 32px; background-color: transparent;")
        content_layout.addWidget(icon_lbl, alignment=Qt.AlignTop)

        msg_lbl = QLabel(text)
        msg_lbl.setWordWrap(True)
        msg_lbl.setStyleSheet("color: #f8fafc; font-size: 13px; font-weight: 500; line-height: 1.4; background-color: transparent;")
        content_layout.addWidget(msg_lbl, 1)

        layout.addLayout(content_layout)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        if is_confirm:
            btn_no = QPushButton("Cancelar")
            btn_no.setObjectName("btnCancel")
            btn_no.clicked.connect(self.reject)
            btn_layout.addWidget(btn_no)

            btn_yes = QPushButton("Sí, Matar Proceso")
            btn_yes.setObjectName("btnConfirm")
            btn_yes.clicked.connect(self.accept)
            btn_layout.addWidget(btn_yes)
        else:
            btn_ok = QPushButton("Aceptar")
            btn_ok.clicked.connect(self.accept)
            btn_layout.addWidget(btn_ok)

        layout.addLayout(btn_layout)

        self.setStyleSheet("""
            QDialog {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 8px;
            }
            QLabel {
                color: #f8fafc;
            }
            QPushButton {
                background-color: #334155;
                color: #ffffff;
                border: 1px solid #475569;
                border-radius: 6px;
                padding: 8px 18px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #475569;
            }
            QPushButton#btnCancel {
                background-color: #475569;
            }
            QPushButton#btnCancel:hover {
                background-color: #64748b;
            }
            QPushButton#btnConfirm {
                background-color: #dc2626;
                border: none;
            }
            QPushButton#btnConfirm:hover {
                background-color: #b91c1c;
            }
        """)


class PortDetailWidget(QWidget):
    """Widget del panel de detalle extendido (columna derecha)."""

    # Señal emitida tras matar un proceso para recargar la lista
    process_killed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_port: Optional[PortInfo] = None
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # Encabezado del puerto seleccionado
        self.title_label = QLabel("📌 Selecciona un puerto para ver su información")
        self.title_label.setObjectName("sectionTitle")
        layout.addWidget(self.title_label)

        # Frame de información del proceso
        self.proc_card = QFrame()
        self.proc_card.setObjectName("cardFrame")
        proc_layout = QVBoxLayout(self.proc_card)

        card_title = QLabel("⚙️ Información del Proceso y Conexión")
        card_title.setStyleSheet("font-weight: bold; color: #38bdf8; font-size: 14px;")
        proc_layout.addWidget(card_title)

        self.lbl_port_proto = QLabel("• Puerto: - | Protocolo: - | Estado: -")
        self.lbl_pid_name = QLabel("• Nombre Proceso: - | PID: -")
        self.lbl_user_exe = QLabel("• Usuario: - | Binario: -")
        self.lbl_cmdline = QLabel("• Comando: -")
        self.lbl_resources = QLabel("• Consumo: -")

        for lbl in [self.lbl_port_proto, self.lbl_pid_name, self.lbl_user_exe, self.lbl_cmdline, self.lbl_resources]:
            lbl.setObjectName("detailLabel")
            lbl.setWordWrap(True)
            proc_layout.addWidget(lbl)

        layout.addWidget(self.proc_card)

        # Frame de Base de Conocimiento Local
        self.kb_card = QFrame()
        self.kb_card.setObjectName("cardFrame")
        kb_layout = QVBoxLayout(self.kb_card)

        kb_title = QLabel("📚 Base de Conocimiento de Ubuntu")
        kb_title.setStyleSheet("font-weight: bold; color: #fbbf24; font-size: 14px;")
        kb_layout.addWidget(kb_title)

        self.lbl_service_cat = QLabel("• Servicio: - | Categoría: - | Riesgo: -")
        self.lbl_service_cat.setObjectName("detailLabel")
        kb_layout.addWidget(self.lbl_service_cat)

        self.desc_box = QTextEdit()
        self.desc_box.setObjectName("descBox")
        self.desc_box.setReadOnly(True)
        self.desc_box.setPlaceholderText("La información explicativa del puerto aparecerá aquí...")
        kb_layout.addWidget(self.desc_box)

        self.lbl_recommendations = QLabel("💡 Recomendación: -")
        self.lbl_recommendations.setObjectName("subtitleLabel")
        self.lbl_recommendations.setWordWrap(True)
        kb_layout.addWidget(self.lbl_recommendations)

        layout.addWidget(self.kb_card)

        # Banner de Advertencia de Proceso Protegido / No Finalizable
        self.lbl_warning_kill = QLabel()
        self.lbl_warning_kill.setWordWrap(True)
        self.lbl_warning_kill.setStyleSheet(
            "color: #fca5a5; background-color: #450a0a; border: 1px solid #991b1b; "
            "border-radius: 6px; padding: 8px 12px; font-size: 12px; font-weight: 500;"
        )
        self.lbl_warning_kill.hide()
        layout.addWidget(self.lbl_warning_kill)

        # Panel de Botones de Acción
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)

        self.btn_kill = QPushButton("🛑 Matar Proceso (SIGKILL)")
        self.btn_kill.setObjectName("btnKill")
        self.btn_kill.setEnabled(False)
        self.btn_kill.clicked.connect(self._on_kill_clicked)
        actions_layout.addWidget(self.btn_kill)

        self.btn_copy = QPushButton("📋 Copiar Info")
        self.btn_copy.setObjectName("btnCopy")
        self.btn_copy.setEnabled(False)
        self.btn_copy.clicked.connect(self._on_copy_clicked)
        actions_layout.addWidget(self.btn_copy)

        layout.addLayout(actions_layout)
        layout.addStretch()

    def display_port(self, port_info: PortInfo):
        """Despliega la información extendida del puerto seleccionado."""
        self._current_port = port_info
        p = port_info

        cat_badge = "🟢 Común Ubuntu (Sistema)" if p.is_common else "🟠 No Común (App / Custom)"
        self.title_label.setText(f"📌 Puerto [{p.protocol} {p.port}] — {p.service_name}")

        # Datos de proceso y validación de seguridad de kill
        if p.process:
            self.lbl_port_proto.setText(f"• Puerto: {p.port} | Protocolo: {p.protocol} | IP: {p.ip_address} | Estado: {p.status}")
            self.lbl_pid_name.setText(f"• Proceso: {p.process.name} | PID: {p.process.pid}")
            self.lbl_user_exe.setText(f"• Usuario: {p.process.username} | Ruta: {p.process.exe_path}")
            self.lbl_cmdline.setText(f"• Comando: {p.process.cmdline}")
            self.lbl_resources.setText(f"• CPU: {p.process.cpu_percent}% | Memoria: {p.process.memory_mb} MB")

            # Evaluar si se puede finalizar el proceso
            check_res = can_terminate_process(p.process.pid)
            if check_res.is_fail():
                self.btn_kill.setEnabled(False)
                self.lbl_warning_kill.setText(f"⚠️ No se puede finalizar este puerto: {check_res.error}")
                self.lbl_warning_kill.show()
            else:
                self.btn_kill.setEnabled(True)
                self.lbl_warning_kill.hide()
        else:
            self.lbl_port_proto.setText(f"• Puerto: {p.port} | Protocolo: {p.protocol} | IP: {p.ip_address} | Estado: {p.status}")
            self.lbl_pid_name.setText("• Proceso: No identificado (Sin PID)")
            self.lbl_user_exe.setText("• Usuario: - | Ruta: -")
            self.lbl_cmdline.setText("• Comando: -")
            self.lbl_resources.setText("• Consumo: -")
            
            self.btn_kill.setEnabled(False)
            self.lbl_warning_kill.setText("⚠️ No se puede finalizar este puerto: No se detectó un PID asociado (Ejecuta la app con 'sudo' para mayor visibilidad).")
            self.lbl_warning_kill.show()

        # Base de Conocimiento
        self.lbl_service_cat.setText(f"• Servicio: {p.service_name} | Tipo: {cat_badge} | Riesgo: {p.risk_level}")
        self.desc_box.setText(f"<b>Resumen:</b> {p.summary}<br><br><b>Descripción Explicativa:</b><br>{p.description}")
        self.lbl_recommendations.setText(f"💡 <b>Recomendación:</b> {p.recommendations}")

        self.btn_copy.setEnabled(True)

    def _on_kill_clicked(self):
        """Maneja el clic en Matar Proceso con confirmación de seguridad."""
        if not self._current_port or not self._current_port.process:
            return

        proc = self._current_port.process
        dialog = CustomDialog(
            self,
            title="Confirmar Finalización de Proceso",
            text=f"¿Estás seguro de que deseas finalizar el proceso '{proc.name}' (PID {proc.pid}) ocupando el puerto {self._current_port.port}?\n\nEsta acción enviará una señal SIGKILL.",
            icon_symbol="⚠️",
            is_confirm=True
        )

        if dialog.exec_() == QDialog.Accepted:
            res = terminate_process(proc.pid, force=True)
            if res.is_ok():
                success_dlg = CustomDialog(
                    self,
                    title="Proceso Finalizado",
                    text=res.value,
                    icon_symbol="✅",
                    is_confirm=False
                )
                success_dlg.exec_()
                self.process_killed.emit()
            else:
                err_dlg = CustomDialog(
                    self,
                    title="Error al Matar Proceso",
                    text=res.error,
                    icon_symbol="❌",
                    is_confirm=False
                )
                err_dlg.exec_()

    def _on_copy_clicked(self):
        """Copia la información técnica extendida del puerto al portapapeles."""
        if not self._current_port:
            return

        p = self._current_port
        proc_str = f"PID: {p.process.pid}, Nombre: {p.process.name}, Comando: {p.process.cmdline}" if p.process else "Sin PID"
        text = (
            f"Puerto: {p.port} ({p.protocol})\n"
            f"Estado: {p.status}\n"
            f"Servicio: {p.service_name}\n"
            f"Proceso: {proc_str}\n"
            f"Resumen: {p.summary}\n"
            f"Descripción: {p.description}\n"
        )
        QApplication.clipboard().setText(text)
        copy_dlg = CustomDialog(
            self,
            title="Copiado",
            text="Información del puerto copiada al portapapeles.",
            icon_symbol="📋",
            is_confirm=False
        )
        copy_dlg.exec_()
