"""
Result Pattern Module
Estándar funcional para retornos seguros de operaciones sin lanzar excepciones descontroladas.
"""

from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

T = TypeVar('T')
E = TypeVar('E')


@dataclass
class Result(Generic[T, E]):
    """
    Representa el resultado de una operación que puede ser exitosa (ok) o fallida (fail).
    """
    success: bool
    value: Optional[T] = None
    error: Optional[E] = None

    @classmethod
    def ok(cls, value: T) -> 'Result[T, E]':
        return cls(success=True, value=value, error=None)

    @classmethod
    def fail(cls, error: E) -> 'Result[T, E]':
        return cls(success=False, value=None, error=error)

    def is_ok(self) -> bool:
        return self.success

    def is_fail(self) -> bool:
        return not self.success
