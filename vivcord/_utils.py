from __future__ import annotations

import functools
from typing import TYPE_CHECKING, ParamSpec, TypeVar

from loguru import logger

if TYPE_CHECKING:
    from typing import Callable


ReturnT = TypeVar("ReturnT")
ParamS = ParamSpec("ParamS")


def call_logger(func: Callable[ParamS, ReturnT]) -> Callable[ParamS, ReturnT]:
    """
    Log calls made to the decorated function.

    Args:
        func (Callable[ParamS, ReturnT]): Function to log calls on

    Returns:
        Callable[ParamS, ReturnT]: The wrapped function
    """

    @functools.wraps(func)
    def wrapper(*args: ParamS.args, **kwargs: ParamS.kwargs) -> ReturnT:
        logger.debug(f"{func.__name__}: {args}, {kwargs}")
        return func(*args, **kwargs)

    return wrapper
