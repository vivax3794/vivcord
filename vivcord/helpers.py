"""Various generic helper functions for internal use."""

from typing import TypeVar

from loguru import logger

V = TypeVar("V")


def check_expected_value(value: V | None, fallback: V) -> V:
    """
    Check that that a value is not None.

    if A value turns out to be none log a warning and return the fallback.

    Args:
        value (V): Value to check.
        fallback (V): Fallback in case value is None

    Returns:
        V: fallback if value is None else value
    """
    if value is None:
        logger.warning(f"Expected value is None, using fallback: {fallback}")
        return fallback
    return value


def fail_if_none(value: V | None, error: BaseException) -> V:
    """
    Raise a error if value is None.

    Args:
        value (V): Value to check
        error (BaseException): Error to raise in the case of a error

    Raises:
        error: The error based in

    Returns:
        V: The value passed in
    """
    if value is None:
        raise error

    return value
