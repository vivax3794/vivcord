"""Command context objects for responding to interactions."""

from __future__ import annotations

import typing
from enum import IntEnum
from typing import TYPE_CHECKING

from loguru import logger

from vivcord import _typed_dicts as type_dicts
from vivcord import commands, datatypes, events, helpers

if TYPE_CHECKING:
    from typing import TypeAlias

    from vivcord.client import Client


class InteractionType(IntEnum):
    """The type of interaction."""

    ping = 1
    application_command = 2
    message_component = 3
    application_command_autocomplete = 4


class ApplicationCommandType(IntEnum):
    """The type of command."""

    slash_command = 1
    user = 2
    message = 3


OPTION_VALS: TypeAlias = (
    str
    | int
    | bool
    | float
    | datatypes.User
    | datatypes.Member
    | datatypes.Channel
    | datatypes.Role
)


class _InteractionContext(events.Event):
    """A general interaction context."""

    def __init__(self, client: Client, data: type_dicts.InteractionEventData) -> None:
        """
        Create a general interaction context.

        Args:
            client (Client): Vivcord client
            data (type_dicts.InteractionEventData): Interaction event data
        """
        self._client = client

        self.type = InteractionType(data["type"])
        self._id = data["id"]
        self._token = data["token"]
        self.guild_id = data.get("guild_id")
        self.channel_id = data.get("channel_id")

        self.member = (
            datatypes.Member(client, data["member"]) if "member" in data else None
        )
        self.user = datatypes.User(client, data["user"]) if "user" in data else None

    async def handle_interaction(self) -> None:
        """
        Handle the interaction.

        This should be overwritten by subclasses to provided command specific actions.

        Raises:
            NotImplementedError: Should be implemented by subclass.
        """
        raise NotImplementedError()


class ApplicationCommandContext(_InteractionContext):
    """Interaction context for a application command."""

    def __init__(self, client: Client, data: type_dicts.InteractionEventData) -> None:
        """
        Create a application command interaction context.

        Args:
            client (Client): Vivcord client
            data (type_dicts.InteractionEventData): Interaction event data

        Raises:
            ValueError: interaction data missing
        """
        super().__init__(client, data)

        int_data = data.get("data")
        if int_data is None:
            raise ValueError("interaction data missing")
        self._int_data = int_data

        self._name = helpers.check_expected_value(int_data.get("name"), "")
        self._type = ApplicationCommandType(
            helpers.check_expected_value(int_data.get("type"), -1)
        )

    async def send(self, data: datatypes.SendMessageData) -> None:
        """
        Send response to interaction.

        Args:
            data (datatypes.SendMessageData): Response data to use.
        """
        await self._client.api.respond_to_interaction(
            self._id, self._token, {"type": 4, "data": data.convert_to_dict()}
        )


class SlashCommandContext(ApplicationCommandContext):
    """Interaction context for a slash command."""

    def __init__(self, client: Client, data: type_dicts.InteractionEventData) -> None:
        """
        Create a slash command interaction context.

        Args:
            client (Client): Vivcord client
            data (type_dicts.InteractionEventData): Interaction event data

        Raises:
            ValueError: unknown argument gotten
        """
        super().__init__(client, data)

        self._resolved = self._int_data.get("resolved")
        self._arguments: dict[str, OPTION_VALS] = {}

        for value in self._int_data.get("options", []):
            option_value = value.get("value", 0)
            logger.debug(
                f"parsing argument {value['name']} with data: {option_value!r} of type {value['type']}"
            )

            user_given_value = OPTION_VALS
            type_ = value["type"]

            if type_ in {3, 4, 10}:
                user_given_value = option_value
            else:
                option_value = typing.cast(int, option_value)
                # when we got this type of value we know we have values in the resolved dict!
                self._resolved = typing.cast(type_dicts.ResolvedData, self._resolved)

                match value["type"]:
                    case 6:
                        if option_value in self._resolved.get("users", {}):
                            user_given_value = datatypes.User(
                                client,
                                helpers.fail_if_none(
                                    self._resolved.get("users"),
                                    KeyError("Expected users key"),
                                )[option_value],
                            )
                        else:
                            user_given_value = datatypes.Member(
                                client,
                                helpers.fail_if_none(
                                    self._resolved.get("members"),
                                    KeyError("Expected members key"),
                                )[option_value],
                            )
                    case 7:
                        user_given_value = datatypes.Channel(
                            client,
                            helpers.fail_if_none(
                                self._resolved.get("channels"),
                                KeyError("Expected channels key"),
                            )[option_value],
                        )
                    case 8:
                        user_given_value = datatypes.Role(
                            client,
                            helpers.fail_if_none(
                                self._resolved.get("roles"),
                                KeyError("Expected roles key"),
                            )[option_value],
                        )
                    case 9:
                        if option_value in self._resolved.get("users", {}):
                            user_given_value = datatypes.User(
                                client,
                                helpers.fail_if_none(
                                    self._resolved.get("users"),
                                    KeyError("Expected users key"),
                                )[option_value],
                            )
                        else:
                            user_given_value = datatypes.Role(
                                client,
                                helpers.fail_if_none(
                                    self._resolved.get("roles"),
                                    KeyError("Expected roles key"),
                                )[option_value],
                            )
                    case _:
                        raise ValueError(f"Unknown option type {value['type']}")

            self._arguments[value["name"]] = user_given_value

    async def handle_interaction(self) -> None:
        """
        Execute slash command callback.

        Raises:
            KeyError: Provided name not found in client.
            TypeError: Command found, but was not a slash command
        """
        command = self._client.get_command(self._name)
        if command is None:
            raise KeyError(f"application command {self._name!r} not found!")
        if not isinstance(command, commands.SlashCommand):
            raise TypeError("expected slash command")

        arguments: list[OPTION_VALS | None] = [
            self._arguments.get(option.name) for option in command.options
        ]

        await command.func(self, *arguments)


@events.event_map_manager.register_type("INTERACTION_CREATE")  # type: ignore
def parse_interaction(
    client: Client, data: type_dicts.InteractionEventData
) -> _InteractionContext:
    """
    Parse interaction event into a context.

    Args:
        client (Client): Vivcord client
        data (type_dicts.InteractionEventData): Event data

    Raises:
        KeyError: Data key not found in event data
        ValueError: unknown application command type
        ValueError: unknown interaction type

    Returns:
        _InteractionContext: The created interaction context
    """
    interaction_type = data["type"]
    match interaction_type:
        case 2:
            if "data" not in data:
                raise KeyError("missing data key in interaction payload.")

            interaction_data = data["data"]
            command_type = interaction_data["type"]

            match command_type:
                case 1:
                    return SlashCommandContext(client, data)
                case _:
                    raise ValueError(
                        f"unknown application command type {command_type!r}"
                    )
        case _:
            raise ValueError(f"unknown interaction type {interaction_type!r}")
