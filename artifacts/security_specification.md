# Especificación de Seguridad & Protección del Sistema
## System: Ubuntu Port Inspector

> *"Tranquilo viejo, aquí las rosquillas están a salvo y los procesos del sistema operativo también. Nada de matar el PID 1 por accidente."* — **Jefe Gorgory**

---

## 🛡️ 1. Reglas de Protección de Procesos del Sistema (Critical PID Shield)

### PIDs y Procesos Protegidos (Lista Negra de Kill)
Se prohíbe explícitamente enviar señales `SIGTERM` / `SIGKILL` a los siguientes PIDs o nombres de proceso:
- **PID 1** (`systemd` / `init`): Proceso raíz del sistema operativo.
- **Procesos Kernel / Sistema Crítico**: `kthreadd`, `systemd-journald`, `systemd-logind`, `dbus-daemon`, `Xorg`, `wayland`.
- **Validación en Código**:
  ```python
  PROTECTED_PIDS = {0, 1}
  PROTECTED_PROCESSES = {
      "systemd", "init", "kthreadd", "systemd-journald", 
      "systemd-logind", "dbus-daemon", "Xorg", "gnome-shell"
  }

  def can_kill_process(pid: int, name: str) -> tuple[bool, str]:
      if pid in PROTECTED_PIDS:
          return False, f"El PID {pid} es un proceso núcleo del sistema y está protegido."
      if name.lower() in PROTECTED_PROCESSES:
          return False, f"El proceso '{name}' es crítico para Ubuntu y no puede ser finalizado."
      return True, ""
  ```

---

## 🔒 2. Diálogo de Confirmación & Elevación de Privilegios

1. **Confirmación Visual Explicita**:
   - Todo intento de finalizar un proceso despliega un cuadro de diálogo nativo (`QMessageBox.warning`) mostrando: Nombre del proceso, PID, usuario ejecutor y puerto afectado.
2. **Manejo Gradual de Señales**:
   - **Paso 1**: Intentar `SIGTERM` (`os.kill(pid, signal.SIGTERM)`) para permitir al proceso liberar recursos limpiamente.
   - **Paso 2**: Si el proceso no responde tras 2 segundos, ofrecer `SIGKILL` (`signal.SIGKILL`).
3. **Gestión de Permisos Linux**:
   - Si el usuario ejecuta la app sin privilegios de administrador y el PID pertenece a otro usuario (`root` / `www-data`), capturar `PermissionError` y mostrar un mensaje instructivo para ejecutar la aplicación con `pkexec` o `sudo`.
