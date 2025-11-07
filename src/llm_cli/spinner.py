from typing import ContextManager

from yaspin import yaspin


def optional_spinner(use_spinner: bool) -> ContextManager:
    return yaspin() if use_spinner else NoopSpinner()


class NoopSpinner:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
