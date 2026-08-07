"""
Process Manager Module
Gestor seguro de procesos para cerrar puertos y finalizar ejecuciones en Ubuntu Linux.
"""

import os
import signal
import psutil
from src.utils.result import Result

# PIDs y nombres protegidos del núcleo de Linux (Ubuntu) y macOS
PROTECTED_PIDS = {0, 1}
PROTECTED_PROCESS_NAMES = {
    # Linux (Ubuntu)
    "systemd", "init", "kthreadd", "systemd-journald",
    "systemd-logind", "dbus-daemon", "xorg", "wayland", "gnome-shell",
    # macOS
    "launchd", "kernel_task", "windowserver", "syslogd",
    "opendirectoryd", "powerd", "logd", "useractivityd"
}


def can_terminate_process(pid: int) -> Result[bool, str]:
    """Verifica si un PID es seguro de finalizar sin poner en riesgo el sistema operativo."""
    if pid in PROTECTED_PIDS:
        return Result.fail(f"El PID {pid} es un proceso fundamental del sistema y no puede ser finalizado.")
    
    try:
        proc = psutil.Process(pid)
        proc_name = proc.name().lower()
        if proc_name in PROTECTED_PROCESS_NAMES:
            return Result.fail(f"El proceso '{proc_name}' (PID {pid}) es un componente crítico del sistema operativo.")
        return Result.ok(True)
    except psutil.NoSuchProcess:
        return Result.fail(f"El proceso con PID {pid} ya no existe en el sistema.")
    except Exception as e:
        return Result.fail(f"Error al verificar la seguridad del PID {pid}: {str(e)}")


def terminate_process(pid: int, force: bool = False) -> Result[str, str]:
    """
    Finaliza el proceso especificado.
    Si force is False, envía SIGTERM. Si force is True, envía SIGKILL.
    """
    check_res = can_terminate_process(pid)
    if check_res.is_fail():
        return Result.fail(check_res.error)

    try:
        proc = psutil.Process(pid)
        proc_name = proc.name()

        sig = signal.SIGKILL if force else signal.SIGTERM
        sig_name = "SIGKILL (Forzado)" if force else "SIGTERM (Limpio)"
        
        proc.send_signal(sig)
        return Result.ok(f"Se envió la señal {sig_name} al proceso '{proc_name}' (PID {pid}) exitosamente.")

    except psutil.NoSuchProcess:
        return Result.ok(f"El proceso PID {pid} ya ha sido finalizado.")
    except psutil.AccessDenied:
        return Result.fail(f"Permisos insuficientes para finalizar el PID {pid}. Ejecuta la aplicación con privilegios sudo.")
    except Exception as e:
        return Result.fail(f"No se pudo finalizar el proceso PID {pid}: {str(e)}")
