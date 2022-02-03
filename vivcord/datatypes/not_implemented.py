"""Not yet implemented attr."""

from loguru import logger


class ToBeImplemented:
    """Not yet implemented attr."""

    def __init__(self) -> None:
        """Produce a warning that a ToBeImplemented object was created."""
        logger.warning("Not yet implemented.")

    def __str__(self) -> str:
        return "ToBeImplemented()"
