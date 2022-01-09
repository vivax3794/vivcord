"""VivCord client."""

from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import TYPE_CHECKING, Any, Callable, Coroutine, TypeVar

import aiohttp

from . import events, context
from ._api import Api
from ._gateway import Gateway
from .taskmanager import TaskManger

if TYPE_CHECKING:
    from typing import TypeAlias

    from . import _internal_types as internal
    from . import datatypes, traits
    from .datatypes import Snowflake

EventT = TypeVar("EventT", bound=events.Event)
EventCallback: TypeAlias = Callable[[EventT], Coroutine[Any, Any, None]]


class Client:
    """VivCord client."""

    def __init__(self, default_guild_id: Snowflake | int | None = None) -> None:
        """
        Create a client.

        Args:
            default_guild_id (Snowflake, optional): A guild id to use for commands.. Defaults to None.
        """
        self.default_guild_id = default_guild_id

        self.api: Api = None  # type: ignore
        self._gateway: Gateway = None  # type: ignore

        self._event_handlers: defaultdict[  # noqa: TAE002
            type[events.Event],
            list[EventCallback[events.Event]],
        ] = defaultdict(list)

        self._commands: dict[str, traits.ApplicationCommand] = {}

        self.task_manger = TaskManger()

    async def _register_commands(self) -> None:
        """Register all slash commnands with the api."""
        global_commands: list[internal.CommandStructure] = []
        guild_commands: dict[int, list[internal.CommandStructure]] = defaultdict(list)

        for command in self._commands.values():
            if command.guild_id is None:
                global_commands.append(command.convert_to_dict())
            else:
                guild_commands[int(command.guild_id)].append(command.convert_to_dict())

        await self.api.overwrite_global_commands(global_commands)

        for guild_id, commands in guild_commands.items():
            await self.api.overwrite_guild_commands(guild_id, commands)

    async def start(self, oauth: str, intents: datatypes.Intents) -> None:
        """
        Start the client.

        This call will never return.

        Args:
            oauth (str): The discord token
            intents (datatypes.Intents): The discord intents to use
        """
        headers = {"Authorization": f"Bot {oauth}"}
        session = aiohttp.ClientSession(headers=headers)

        self.api = Api(session)

        gateway_url = await self.api.get_gateway()
        self._gateway = Gateway(self, session)

        self.task_manger.add_task(self._gateway.start(gateway_url, oauth, intents))

        try:
            await self.task_manger.start()
        finally:
            await self.close()

    def run(self, oauth: str, intents: datatypes.Intents) -> None:
        """
        Start the client.

        This call will never return.

        Args:
            oauth (str): The discord token
            intents (datatypes.Intents): The discord intents to use
        """
        asyncio.run(self.start(oauth, intents))

    async def close(self) -> None:
        """Close down the client."""
        await self.task_manger.close()

        await self._gateway.close()
        await self.api.session.close()

    async def handle_event(self, event: events.Event) -> None:
        """
        Handle a incoming event.

        Args:
            event (events.Event): The event that happend.
        """
        if isinstance(event, events.Ready):
            self.api.application_id = event.application.id_
            await self._register_commands()
        
        elif isinstance(event, context._ApplicationCommandContext):
            await event.call_callback()

        tasks: list[Coroutine[Any, Any, None]] = [
            callback(event) for callback in self._event_handlers[type(event)]
        ]
        _ = await asyncio.gather(*tasks)

    def register_handler(
        self,
        event_type: type[EventT],
        callback: EventCallback[EventT],
    ) -> None:
        """
        Regsiter a callback handler.

        Args:
            event_type (type[EventT]): Event the callback should respond to
            callback (EventCallback[EventT]): Callback that will be called when the event happens
        """
        self._event_handlers[event_type].append(callback)

    def on_event(
        self, event_type: type[EventT]
    ) -> Callable[[EventCallback[EventT]], EventCallback[EventT]]:
        """
        Register a event handler using decorators.

        Args:
            event_type (type[EventT]): The type to register on

        Returns:
            Callable[[EventCallback[EventT]], EventCallback[EventT]]: The decorator that should be used.
        """

        def decorator(callback: EventCallback[EventT]) -> EventCallback[EventT]:
            self.register_handler(event_type, callback)
            return callback

        return decorator

    def register_command(self, command: traits.ApplicationCommand) -> None:
        if command.guild_id is None:
            command.guild_id = self.default_guild_id

        self._commands[command.name] = command
    
    def get_command(self, name: str) -> traits.ApplicationCommand | None:
        return self._commands.get(name)