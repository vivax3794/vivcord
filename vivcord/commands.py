"""Discord interactions."""

from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Coroutine,
    Generic,
    ParamSpec,
    TypeVar,
    Concatenate
)

from . import datatypes, traits

if TYPE_CHECKING:
    from typing import TypeAlias

    from . import _internal_types as internal
    from . import context

ChoiceT = TypeVar("ChoiceT", str, int, float)
OptionT = TypeVar("OptionT")
ParamS = ParamSpec("ParamS")

CommandCallback: TypeAlias = Callable[Concatenate["context.SlashCommandContext", ParamS], Coroutine[Any, Any, None]]
AutocompleteFunc: TypeAlias = Callable[[str], list["CommandChoice[ChoiceT]"]]


class _SlashCommand(Generic[ParamS]):
    def __init__(
        self,
        name: str,
        description: str,
        default_permission: bool,
        guild_id: datatypes.Snowflake | int | None,
        func: CommandCallback[ParamS],
    ) -> None:
        self.name = name
        self.description = description
        self.default_permission = default_permission
        self.guild_id = guild_id
        self.func = func

        self.options: list[traits.CommandOption[Any]] = []

    def convert_to_dict(self: _SlashCommand[[]]) -> internal.CommandStructure:
        return {
            "type": 1,
            "name": self.name,
            "description": self.description,
            "default_permission": self.default_permission,
            "options": [option.convert_to_dict() for option in self.options],
        }


class CommandChoice(Generic[ChoiceT]):
    """A command Choice."""

    def __init__(self, name: str, value: ChoiceT) -> None:
        """
        Create a command choice.

        Args:
            name (str): The choice name
            value (ChoiceT): The choice description
        """
        self.name = name
        self.value = value

    def convert_to_dict(self) -> internal.CommandChoice:
        """
        Convert choice to dict.

        Returns:
            internal.CommandChoice: The resulting dict.
        """
        return {"name": self.name, "value": self.value}


class CommandOptionString(traits.CommandOption[str]):
    """A string option."""

    def __init__(
        self,
        name: str,
        description: str,
        required: bool = True,
        choices: list[CommandChoice[str]] | None = None,
        autocomplete: AutocompleteFunc[str] | None = None,
    ) -> None:
        """
        Create a CommandOptionString.

        Args:
            name (str): The option name.
            description (str): The option description.
            required (bool): Wether the option is required. Defaults to True.
            choices (list[CommandChoice[str]], optional): List of set options the user name pick from. Defaults to None.
            autocomplete (AutocompleteFunc[str], optional): A callback function for autocomplete. Defaults to None.
        """
        super().__init__(name, description)
        self.required = required
        self.choices = choices
        self.autocomplete = autocomplete

    def convert_to_dict(self) -> internal.CommandOption:
        """
        Convert the option to a dict.

        Returns:
            internal.CommandOption: The resulting dict
        """
        data: internal.CommandOption = {
            "type": 3,
            "name": self.name,
            "description": self.description,
            "required": self.required,
        }

        if self.choices is not None:
            data["choices"] = [choice.convert_to_dict() for choice in self.choices]

        if self.autocomplete is not None:
            data["autocomplete"] = True

        return data


class CommandOptionInt(traits.CommandOption[int]):
    """A int option."""

    def __init__(
        self,
        name: str,
        description: str,
        required: bool = True,
        choices: list[CommandChoice[int]] | None = None,
        min_value: int | None = None,
        max_value: int | None = None,
        autocomplete: AutocompleteFunc[int] | None = None,
    ) -> None:
        """
        Create a CommandOptionInt.

        Args:
            name (str): The option name.
            description (str): The describtion name.
            required (bool): Wether this option is required. Defaults to True.
            choices (list[CommandChoice[int]], optional): Choices user has to choose from. Defaults to None.
            min_value (int, optional): Minimum value of int. Defaults to None.
            max_value (int, optional): Maximum value of int. Defaults to None.
            autocomplete (AutocompleteFunc[int], optional): Callback for autocomplete. Defaults to None.
        """
        super().__init__(name, description)
        self.required = required
        self.choices = choices
        self.min_value = min_value
        self.max_value = max_value
        self.autocomplete = autocomplete

    def convert_to_dict(self) -> internal.CommandOption:
        """
        Convert the option to a dict.

        Returns:
            internal.CommandOption: The resulting dict
        """
        data: internal.CommandOption = {
            "type": 4,
            "name": self.name,
            "description": self.description,
            "required": self.required,
        }

        if self.choices is not None:
            data["choices"] = [choice.convert_to_dict() for choice in self.choices]

        if self.min_value is not None:
            data["min_value"] = self.min_value

        if self.max_value is not None:
            data["max_value"] = self.max_value

        if self.autocomplete is not None:
            data["autocomplete"] = True

        return data


class CommandOptionBoolean(traits.CommandOption[bool]):
    """True or False option."""

    def __init__(self, name: str, description: str, required: bool = True) -> None:
        """
        Create CommandOptionBoolean.

        Args:
            name (str): Name of option
            description (str): Option description
            required (bool): Wether it is required. Defaults to True.
        """
        super().__init__(name, description)
        self.required = required

    def convert_to_dict(self) -> internal.CommandOption:
        """
        Convert the option to a dict.

        Returns:
            internal.CommandOption: The resulting dict
        """
        return {
            "type": 5,
            "name": self.description,
            "description": self.description,
            "required": self.required,
        }


class CommandOptionUser(traits.CommandOption[datatypes.User | datatypes.Member]):
    """Option taking a discord user."""

    def __init__(self, name: str, description: str, required: bool = True) -> None:
        """
        Create CommandOptionUser.

        Args:
            name (str): Name of option
            description (str): Option description
            required (bool): Wether it is required. Defaults to True.
        """
        super().__init__(name, description)
        self.required = required

    def convert_to_dict(self) -> internal.CommandOption:
        """
        Convert the option to a dict.

        Returns:
            internal.CommandOption: The resulting dict
        """
        return {
            "type": 6,
            "name": self.name,
            "description": self.description,
            "required": self.required,
        }


class CommandOptionChannel(traits.CommandOption[datatypes.Channel]):
    """Option taking a discord channel."""

    def __init__(
        self,
        name: str,
        description: str,
        required: bool = True,
        channel_types: list[datatypes.ChannelType] | None = None,
    ) -> None:
        """
        Create CommandOptionChannel.

        Args:
            name (str): Name of the option
            description (str): The option description
            required (bool): Wether it is required. Defaults to True.
            channel_types (list[datatypes.ChannelType], optional): Allowed channel types. Defaults to None.
        """
        super().__init__(name, description)
        self.required = required
        self.channel_types = channel_types

    def convert_to_dict(self) -> internal.CommandOption:
        """
        Convert the option to a dict.

        Returns:
            internal.CommandOption: The resulting dict
        """
        data: internal.CommandOption = {
            "type": 7,
            "name": self.name,
            "description": self.description,
            "required": self.required,
        }

        if self.channel_types is not None:
            data["channel_types"] = [
                channel_type.value for channel_type in self.channel_types
            ]

        return data


class CommandOptionRole(traits.CommandOption[datatypes.Role]):
    """Option taking a discord role."""

    def __init__(self, name: str, description: str, required: bool = True) -> None:
        """
        Create CommandOptionRole.

        Args:
            name (str): Name of option
            description (str): Option description
            required (bool): Wether it is required. Defaults to True.
        """
        super().__init__(name, description)
        self.required = required

    def convert_to_dict(self) -> internal.CommandOption:
        """
        Convert the option to a dict.

        Returns:
            internal.CommandOption: The resulting dict
        """
        return {
            "type": 8,
            "name": self.name,
            "description": self.description,
            "required": self.required,
        }


class CommandOptionMentionable(
    traits.CommandOption[datatypes.User | datatypes.Member | datatypes.Role]
):
    """Option taking a discord role or user."""

    def __init__(self, name: str, description: str, required: bool = True) -> None:
        """
        Create CommandOptionMentionable.

        Args:
            name (str): Name of option
            description (str): Option description
            required (bool): Wether it is required. Defaults to True.
        """
        super().__init__(name, description)
        self.required = required

    def convert_to_dict(self) -> internal.CommandOption:
        """
        Convert the option to a dict.

        Returns:
            internal.CommandOption: The resulting dict
        """
        return {
            "type": 9,
            "name": self.name,
            "description": self.description,
            "required": self.required,
        }


class CommandOptionFloat(traits.CommandOption[float]):
    """Option taking a float."""

    def __init__(
        self,
        name: str,
        description: str,
        required: bool = True,
        choices: list[CommandChoice[float]] | None = None,
        min_value: float | None = None,
        max_value: float | None = None,
        autocomplete: AutocompleteFunc[float] | None = None,
    ) -> None:
        """
        Create a CommandOptionFloat.

        Args:
            name (str): The option name.
            description (str): The describtion name.
            required (bool): Wether this option is required. Defaults to True.
            choices (list[CommandChoice[int]], optional): Choices user has to choose from. Defaults to None.
            min_value (int, optional): Minimum value of int. Defaults to None.
            max_value (int, optional): Maximum value of int. Defaults to None.
            autocomplete (AutocompleteFunc[int], optional): Callback for autocomplete. Defaults to None.
        """
        super().__init__(name, description)
        self.required = required
        self.choices = choices
        self.min_value = min_value
        self.max_value = max_value
        self.autocomplete = autocomplete

    def convert_to_dict(self) -> internal.CommandOption:
        """
        Convert the option to a dict.

        Returns:
            internal.CommandOption: The resulting dict
        """
        data: internal.CommandOption = {
            "type": 10,
            "name": self.name,
            "description": self.description,
            "required": self.required,
        }

        if self.choices is not None:
            data["choices"] = [choice.convert_to_dict() for choice in self.choices]

        if self.min_value is not None:
            data["min_value"] = self.min_value

        if self.max_value is not None:
            data["max_value"] = self.max_value

        if self.autocomplete is not None:
            data["autocomplete"] = True

        return data


def slash_command(
    name: str,
    description: str,
    default_permission: bool = True,
    guild_id: int | None = None,
) -> Callable[[CommandCallback[ParamS]], _SlashCommand[ParamS]]:
    """
    Convert function to a slash command.

    Args:
        name (str): Name of command
        description (str): Command description
        default_permission (bool): The default permission for the command. Defaults to True.
        guild_id (int, optional): Guild id if it is a guild only command. Defaults to None.

    Returns:
        Callable[[CommandCallback[ParamS]], _SlashCommand[ParamS]]: Decorator
    """

    def decorator(func: CommandCallback[ParamS]) -> _SlashCommand[ParamS]:
        return _SlashCommand(name, description, default_permission, guild_id, func)

    return decorator


def with_argument(
    option: traits.CommandOption[OptionT],
) -> Callable[[_SlashCommand[Concatenate[OptionT, ParamS]]], _SlashCommand[ParamS]]:
    """
    Add a option to a slash command.

    Args:
        option (traits.CommandOption[OptionT]): Option to add, must match decorated function.

    Returns:
        Callable[[_SlashCommand[Concatenate[OptionT, ParamS]]], _SlashCommand[ParamS]]: Decorator
    """

    def decorator(
        command: _SlashCommand[Concatenate[OptionT, ParamS]]
    ) -> _SlashCommand[ParamS]:
        command.options.append(option)
        return command  # type: ignore

    return decorator
