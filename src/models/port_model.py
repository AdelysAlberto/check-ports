"""
Modelos de Datos para Puertos y Procesos
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ProcessDetail:
    """Detalles extendidos del proceso asociado a un puerto."""
    pid: int
    name: str
    cmdline: str
    username: str
    exe_path: str
    cpu_percent: float
    memory_mb: float


@dataclass
class PortInfo:
    """Información completa de un puerto en escucha o activo."""
    port: int
    protocol: str       # 'TCP' o 'UDP'
    status: str         # 'LISTEN', 'ESTABLISHED', etc.
    ip_address: str
    process: Optional[ProcessDetail]
    is_common: bool
    service_name: str
    summary: str
    description: str
    risk_level: str     # 'BAJO', 'MEDIO', 'ALTO'
    recommendations: str
