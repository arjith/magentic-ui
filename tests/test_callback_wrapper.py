import pytest
from magentic_ui.callback_wrapper import CallbackWrapper


def sample_func(x: int) -> int:
    return x + 1


def test_callback_wrapper_call() -> None:
    wrapper = CallbackWrapper.from_callable(sample_func)
    assert "sample_func" in wrapper.path
    assert wrapper(1) == 2
