from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

from loguru import logger

from . import commands, datatypes, events, helpers

if TYPE_CHECKING:
    from typing import TypeAlias

    from . import _internal_types as internal
    from .client import Client


class InteractionType(IntEnum):
    ping = 1
    application_command = 2
    message_component = 3
    application_command_autocomplete = 4


class ApplicationCommandType(IntEnum):
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


# TODO: class _InteractionContext(traits.Messageable):
class _InteractionContext(events.Event):
    def __init__(self, client: Client, data: internal.InteractionEventData) -> None:
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
        raise NotImplementedError()


class _ApplicationCommandContext(_InteractionContext):
    def __init__(self, client: Client, data: internal.InteractionEventData) -> None:
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
        await self._client.api.respond_to_interaction(
            self._id, self._token, {"type": 4, "data": data.convert_to_dict()}
        )


class SlashCommandContext(_ApplicationCommandContext):
    def __init__(self, client: Client, data: internal.InteractionEventData) -> None:
        super().__init__(client, data)

        self._resolved = self._int_data.get("resolved", {})
        self._arguments: dict[str, OPTION_VALS] = {}

        for value in self._int_data.get("options", []):
            option_value = value.get("value", 0)
            logger.debug(
                f"parsing argument {value['name']} with data: {option_value!r} of type {value['type']}"
            )

            match value["type"]:
                case 3 | 4 | 10:
                    user_given_value = option_value
                case 6:
                    if option_value in self._resolved.get("users", {}):
                        user_given_value = datatypes.User(
                            client,
                            self._resolved["users"][option_value],  # type: ignore
                        )
                    else:
                        user_given_value = datatypes.Member(
                            client,
                            self._resolved["members"][option_value],  # type: ignore
                        )
                case 7:
                    user_given_value = datatypes.Channel(
                        client, self._resolved["channels"][option_value]  # type: ignore
                    )
                case 8:
                    user_given_value = datatypes.Role(
                        client, self._resolved["roles"][option_value]  # type: ignore
                    )
                case 9:
                    if option_value in self._resolved.get("users", {}):
                        user_given_value = datatypes.User(
                            client,
                            self._resolved["users"][option_value],  # type: ignore
                        )
                    else:
                        user_given_value = datatypes.Role(
                            client,
                            self._resolved["roles"][option_value],  # type: ignore
                        )
                case _:
                    raise ValueError(f"Unknown option type {value['type']}")

            self._arguments[value["name"]] = user_given_value

    async def handle_interaction(self) -> None:
        command = self._client.get_command(self._name)
        if command is None:
            raise KeyError(f"application command {self._name!r} not found!")
        if not isinstance(command, commands._SlashCommand):
            raise TypeError("expected slash command")

        arguments: list[OPTION_VALS | None] = []
        for option in command.options:
            arguments.append(self._arguments.get(option.name))

        await command.func(self, *arguments)


@events.event_map_manager.register_type("INTERACTION_CREATE")  # type: ignore
def parse_interaction(
    client: Client, data: internal.InteractionEventData
) -> _InteractionContext:
    match data["type"]:
        case 2:
            match data.get("data", {}).get("type"):
                case 1:
                    return SlashCommandContext(client, data)
                case _:
                    raise ValueError("unknown application command type.")
        case _:
            raise ValueError("unknown interaction type.")
