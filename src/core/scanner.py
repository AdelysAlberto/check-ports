import os
import platform
import shutil
import subprocess
import socket
import psutil
from typing import List, Optional, Set, Tuple
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
            exe_path = "Acceso Denegado (Requiere privilegios)"

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


def _resolve_lsof() -> Optional[str]:
    """
    Resuelve la ruta del binario lsof. En macOS vive en /usr/sbin, ausente del
    PATH cuando la app se lanza desde Finder o launchd con entorno reducido.
    """
    found = shutil.which("lsof")
    if found:
        return found
    for candidate in ("/usr/sbin/lsof", "/sbin/lsof", "/usr/bin/lsof"):
        if os.path.exists(candidate):
            return candidate
    return None


def _scan_via_lsof() -> List[dict]:
    """
    Escaneo nativo usando 'lsof' (ideal para macOS sin privilegios root).
    Captura sockets TCP en LISTEN y UDP activos.
    """
    scanned_list: List[dict] = []
    seen_keys: Set[Tuple[int, str, Optional[int]]] = set()

    lsof_bin = _resolve_lsof()
    if not lsof_bin:
        return []

    try:
        cmd = [lsof_bin, "-nP", "-iTCP", "-sTCP:LISTEN", "-iUDP"]
        output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True)
    except Exception:
        return []

    lines = output.strip().splitlines()
    if len(lines) <= 1:
        return []

    for line in lines[1:]:
        parts = line.split()
        if len(parts) < 9:
            continue

        try:
            pid = int(parts[1])
        except ValueError:
            pid = None

        protocol_raw = parts[4].upper()
        name_col = parts[8] if len(parts) > 8 else ""

        # Determinar protocolo
        protocol = "TCP" if "TCP" in line.upper() or "TCP" in protocol_raw else "UDP"
        status = "LISTEN" if protocol == "TCP" else "UDP"

        # Extraer dirección y puerto desde la columna NAME (ej: *:7000, 127.0.0.1:3000, *:5353)
        if "->" in name_col:
            # Conexión establecida o punto a punto (ignorar o tomar origen)
            target = name_col.split("->")[0]
        else:
            target = name_col

        if ":" not in target:
            continue

        ip_part, port_part = target.rsplit(":", 1)
        if port_part == "*":
            continue

        try:
            port = int(port_part)
        except ValueError:
            continue

        ip_address = ip_part if ip_part != "*" else "0.0.0.0"

        key = (port, protocol, pid)
        if key in seen_keys:
            continue
        seen_keys.add(key)

        proc_detail = _get_process_detail(pid) if pid else None

        scanned_list.append({
            "port": port,
            "protocol": protocol,
            "status": status,
            "ip_address": ip_address,
            "process": proc_detail
        })

    return scanned_list


def scan_active_ports() -> Result[List[dict], str]:
    """
    Escanea todos los puertos TCP y UDP en escucha o activos del sistema (Linux / macOS).
    Usa psutil y recurre automáticamente a lsof en macOS si psutil requiere permisos root.
    """
    # En macOS, intentar primero con lsof o fallback si psutil lanza AccessDenied
    is_macos = platform.system() == "Darwin"

    if is_macos:
        lsof_results = _scan_via_lsof()
        if lsof_results:
            lsof_results.sort(key=lambda x: x["port"])
            return Result.ok(lsof_results)

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

        scanned_list.sort(key=lambda x: x["port"])
        return Result.ok(scanned_list)

    except (PermissionError, psutil.AccessDenied):
        # Fallback secundario a lsof
        lsof_fallback = _scan_via_lsof()
        if lsof_fallback:
            lsof_fallback.sort(key=lambda x: x["port"])
            return Result.ok(lsof_fallback)
        return Result.fail("Permisos insuficientes para inspeccionar las conexiones. Ejecuta la app como administrador o activa el botón Sudo.")
    except Exception as e:
        return Result.fail(f"Error al escanear los puertos del sistema: {str(e)}")

