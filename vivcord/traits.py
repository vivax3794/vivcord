"""Abstract classes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, ParamSpec, Protocol, TypeVar

if TYPE_CHECKING:
    from vivcord import _typed_dicts as type_dicts
    from vivcord import datatypes


T = TypeVar("T")
P = ParamSpec("P")


class ApplicationCommand(Protocol):
    """A discord command."""

    guild_id: datatypes.Snowflake | int | None
    name: str

    def convert_to_dict(self) -> type_dicts.CommandStructure:
        """
        Convert the command to a dict.

        Returns:
            type_dicts.CommandStructure: The resulting dict
        """
        return NotImplemented


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
    def convert_to_dict(self) -> type_dicts.CommandOption:
        """
        Convert the option to a dict.

        Returns:
            type_dicts.CommandOption: The resulting dict
        """
        ...


class Messageable(ABC):
    """This object can have messages sent to it."""

    @abstractmethod
    async def send(self, data: datatypes.SendMessageData) -> None:
        """
        Send message to this object.

        Args:
            data (datatypes.SendMessageData): Message data to send.
        """
