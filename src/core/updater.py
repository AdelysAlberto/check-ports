"""
Updater Module
Comprueba la disponibilidad de nuevas versiones en GitHub y permite la actualización con un clic.
"""

import os
import sys
import json
import urllib.request
import subprocess
from typing import Optional, Tuple
from src.version import __version__, GITHUB_API_RELEASES, GITHUB_API_TAGS
from src.utils.result import Result


def _parse_version(v_str: str) -> Tuple[int, ...]:
    """Limpia y convierte una cadena de versión 'v1.2.3' en tupla de enteros (1, 2, 3)."""
    clean_v = v_str.strip().lstrip('v').lstrip('V')
    parts = []
    for p in clean_v.split('.'):
        digits = ''.join(c for c in p if c.isdigit())
        if digits:
            parts.append(int(digits))
    return tuple(parts) if parts else (0,)


def is_newer_version(current: str, remote: str) -> bool:
    """Compara si la versión remota es mayor a la actual."""
    try:
        return _parse_version(remote) > _parse_version(current)
    except Exception:
        return False


def check_for_updates() -> Result[Optional[str], str]:
    """
    Consulta GitHub para verificar si existe una nueva versión/tag.
    Retorna Result.ok(tag_name) si hay una nueva versión disponible,
    Result.ok(None) si está al día, o Result.fail con el error.
    """
    req_headers = {
        "User-Agent": "CheckPorts-App",
        "Accept": "application/vnd.github.v3+json"
    }

    # 1. Intentar obtener último release
    try:
        req = urllib.request.Request(GITHUB_API_RELEASES, headers=req_headers)
        with urllib.request.urlopen(req, timeout=4) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                remote_tag = data.get("tag_name", "")
                if remote_tag and is_newer_version(__version__, remote_tag):
                    return Result.ok(remote_tag)
                return Result.ok(None)
    except Exception:
        pass

    # 2. Fallback a tags si no se usan releases formales
    try:
        req = urllib.request.Request(GITHUB_API_TAGS, headers=req_headers)
        with urllib.request.urlopen(req, timeout=4) as response:
            if response.status == 200:
                tags = json.loads(response.read().decode('utf-8'))
                if tags and isinstance(tags, list):
                    latest_tag = tags[0].get("name", "")
                    if latest_tag and is_newer_version(__version__, latest_tag):
                        return Result.ok(latest_tag)
                    return Result.ok(None)
    except Exception as e:
        return Result.fail(f"No se pudo verificar actualizaciones: {str(e)}")

    return Result.ok(None)


def perform_update() -> Result[str, str]:
    """
    Ejecuta la actualización del código mediante git pull en el directorio del proyecto.
    """
    app_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    try:
        res = subprocess.run(
            ["git", "pull", "--quiet"],
            cwd=app_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        if res.returncode != 0:
            err = res.stderr.strip() or "Fallo al ejecutar git pull"
            return Result.fail(err)

        return Result.ok("Actualización completada exitosamente.")
    except Exception as e:
        return Result.fail(f"Error durante la actualización: {str(e)}")
