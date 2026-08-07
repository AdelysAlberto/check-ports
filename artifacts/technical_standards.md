# Estándares Técnicos, Clean Code & Result Pattern (Python 3)
## System: Ubuntu Port Inspector

> *"PROCESANDO DATOS TÉCNICOS. SINTAXIS EVALUADA CON PRECISIÓN ROBÓTICA: SE REQUIERE PATRÓN RESULT Y CERO EXCEPCIONES SILENCIOSAS."* — **Vicky (V.I.C.I.)**

---

## 🤖 1. Patrón Result en Python (`src/utils/result.py`)

Para evitar lanzar excepciones descontroladas en el escaneo de puertos y matar procesos, todas las funciones de servicio deben retornar un objeto `Result` explícito:

```python
from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

T = TypeVar('T')
E = TypeVar('E')

@dataclass
class Result(Generic[T, E]):
    success: bool
    value: Optional[T] = None
    error: Optional[E] = None

    @classmethod
    def ok(cls, value: T) -> 'Result[T, E]':
        return cls(success=True, value=value, error=None)

    @classmethod
    def fail(cls, error: E) -> 'Result[T, E]':
        return cls(success=False, value=None, error=error)
```

---

## 🛠️ 2. Convenciones de Código & Rigor Técnico

1. **Tipado Estricto (Type Hints)**:
   - Todas las funciones Python deben incluir anotaciones de tipo (`def scan_ports() -> Result[List[PortInfo], str]:`).
2. **Desacoplamiento UI / Lógica de Sistema**:
   - Ningún widget PySide6 debe realizar llamadas directas a `os.kill` o `psutil` sin pasar por la capa `src/core/`.
3. **Manejo de Errores Silenciosos Prohibido**:
   - `try-except` bloques deben capturar excepciones específicas (`PermissionError`, `psutil.NoSuchProcess`) y retornar un `Result.fail("Mensaje claro")`.
