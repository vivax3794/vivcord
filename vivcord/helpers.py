from typing import TypeVar

from loguru import logger

V = TypeVar("V")


def check_expected_value(value: V | None, fallback: V) -> V:
    if value is None:
        logger.warning(f"Expected value is None, using fallback: {fallback}")
        return fallback
    return value
