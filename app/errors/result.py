from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Generic, NoReturn, TypeAlias, TypeVar

T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
E = TypeVar("E")
E_co = TypeVar("E_co", covariant=True)
U = TypeVar("U")
F = TypeVar("F")
D = TypeVar("D")


@dataclass(frozen=True, slots=True)
class Ok(Generic[T_co]):
    """Successful outcome carrying a value."""

    value: T_co

    @property
    def is_ok(self) -> bool:
        return True

    @property
    def is_err(self) -> bool:
        return False

    def unwrap(self) -> T_co:
        return self.value

    def unwrap_or(self, _default: object) -> T_co:
        return self.value

    def map(self, fn: Callable[[T_co], U]) -> Ok[U]:
        return Ok(fn(self.value))

    def map_err(self, _fn: Callable[[Any], Any]) -> Ok[T_co]:
        return self


@dataclass(frozen=True, slots=True)
class Err(Generic[E_co]):
    """Failed outcome carrying an error (often an exception or structured error)."""

    error: E_co

    @property
    def is_ok(self) -> bool:
        return False

    @property
    def is_err(self) -> bool:
        return True

    def unwrap(self) -> NoReturn:
        if isinstance(self.error, BaseException):
            raise self.error
        raise RuntimeError(str(self.error))

    def unwrap_or(self, default: D) -> D:
        return default

    def map(self, _fn: Callable[[Any], U]) -> Err[E_co]:
        return self

    def map_err(self, fn: Callable[[E_co], F]) -> Err[F]:
        return Err(fn(self.error))


Result: TypeAlias = Ok[T] | Err[E]


def ok(value: T) -> Ok[T]:
    return Ok(value)


def err(error: E) -> Err[E]:
    return Err(error)
