from typing import TypeVar

from loguru import logger

V = TypeVar("V")


def check_expected_value(value: V | None, fallback: V) -> V:
    if value is None:
        logger.warning(f"Expected value is None, using fallback: {fallback}")
        return fallback
    return value


def fail_if_none(value: V | None, error: BaseException) -> V:
    if value is None:
        raise error

    return value
