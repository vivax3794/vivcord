"""Abstract classes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, Protocol, TypeVar

if TYPE_CHECKING:
    from . import _internal_types as internal
    from . import datatypes


T = TypeVar("T")


class ApplicationCommand(Protocol):
    """A discord command."""

    guild_id: datatypes.Snowflake | int | None

    def convert_to_dict(self) -> internal.CommandStructure:
        """
        Convert the command to a dict.

        Returns:
            internal.CommandStructure: The resulting dict
        """
        ...


class CommandOption(ABC, Generic[T]):
    """A option for a slash command."""

    def __init__(self, name: str, description: str) -> None:
        """
        Create a CommandOption.

        Args:
            name (str): The name of the option.
            description (str): The option describtion.
        """
        self.name = name
        self.description = description

    @abstractmethod
    def convert_to_dict(self) -> internal.CommandOption:
        """
        Convert the option to a dict.

        Returns:
            internal.CommandOption: The resulting dict
        """
        ...
