from __future__ import annotations

from typing import Any, Callable, cast
import importlib
from pydantic import BaseModel, field_serializer, field_validator


class CallbackWrapper(BaseModel):
    """Serializable wrapper around a callback function."""

    path: str
    model_config = {"arbitrary_types_allowed": True}

    @field_validator("path", mode="before")
    @classmethod
    def _validate_path(cls, v: str | Callable[..., Any]) -> str:
        if callable(v):
            return f"{v.__module__}.{getattr(v, '__qualname__', v.__name__)}"
        if isinstance(v, str):
            return v
        raise TypeError("Invalid callback value")

    @field_serializer("path")
    def _serialize_path(self, path: str) -> str:
        return path

    def _load(self) -> Callable[..., Any]:
        module_path, attr = self.path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        func = module
        for part in attr.split("."):
            func = getattr(func, part)
        if not callable(func):
            raise TypeError("Callback target is not callable")
        return func

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self._load()(*args, **kwargs)

    @classmethod
    def from_callable(cls, func: Callable[..., Any]) -> "CallbackWrapper":
        return cls(path=cast(str, func))
