"""
Scanner Module
Inspecciona los sockets y puertos de red activos en el sistema Ubuntu mediante psutil.
"""

import socket
import psutil
from typing import List, Optional
from src.models.port_model import ProcessDetail, PortInfo
from src.utils.result import Result


def _get_process_detail(pid: int) -> Optional[ProcessDetail]:
    """Obtiene los detalles técnicos de un proceso dado su PID."""
    if not pid:
        return None
    try:
        proc = psutil.Process(pid)
        name = proc.name()
        
        try:
            cmdline = " ".join(proc.cmdline()) or name
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            cmdline = name
            
        try:
            username = proc.username()
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            username = "Desconocido"

        try:
            exe_path = proc.exe() or "N/A"
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            exe_path = "Acceso Denegado (Requiere sudo)"

        try:
            cpu_percent = proc.cpu_percent(interval=0.0)
            mem_info = proc.memory_info()
            memory_mb = round(mem_info.rss / (1024 * 1024), 2)
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            cpu_percent = 0.0
            memory_mb = 0.0

        return ProcessDetail(
            pid=pid,
            name=name,
            cmdline=cmdline,
            username=username,
            exe_path=exe_path,
            cpu_percent=cpu_percent,
            memory_mb=memory_mb
        )
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None


def scan_active_ports() -> Result[List[dict], str]:
    """
    Escanea todos los puertos TCP y UDP en escucha o activos del sistema Ubuntu.
    Retorna una lista de diccionarios con la información básica detectada por el SO.
    """
    try:
        connections = psutil.net_connections(kind='inet')
        scanned_list: List[dict] = []
        seen_keys = set()

        for conn in connections:
            if conn.status != psutil.CONN_LISTEN and conn.type != socket.SOCK_DGRAM:
                continue

            laddr = conn.laddr
            if not laddr:
                continue

            port = laddr.port
            ip_address = laddr.ip
            protocol = "TCP" if conn.type == socket.SOCK_STREAM else "UDP"
            status = conn.status if conn.status else "UDP"

            # Clave única para evitar duplicados idénticos
            key = (port, protocol, conn.pid)
            if key in seen_keys:
                continue
            seen_keys.add(key)

            proc_detail = _get_process_detail(conn.pid) if conn.pid else None

            scanned_list.append({
                "port": port,
                "protocol": protocol,
                "status": status,
                "ip_address": ip_address,
                "process": proc_detail
            })

        # Ordenar por número de puerto
        scanned_list.sort(key=lambda x: x["port"])
        return Result.ok(scanned_list)

    except PermissionError:
        return Result.fail("Permisos insuficientes para inspeccionar las conexiones del sistema. Ejecuta la app con privilegios.")
    except Exception as e:
        return Result.fail(f"Error al escanear los puertos del sistema: {str(e)}")
