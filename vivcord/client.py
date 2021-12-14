"""VivCord client."""

from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import TYPE_CHECKING, Any, Callable, Coroutine, TypeVar

import aiohttp

from . import events
from ._api import Api
from ._gateway import Gateway

if TYPE_CHECKING:
    from typing import TypeAlias

    from . import datatypes

EventT = TypeVar("EventT", bound=events.Event)
EventCallback: TypeAlias = Callable[[EventT], Coroutine[Any, Any, None]]


class Client:
    """VivCord client."""

    def __init__(self) -> None:
        """Create a client."""
        self._api: Api = None  # type: ignore
        self._gateway: Gateway = None  # type: ignore

        self._event_handlers: defaultdict[  # noqa: TAE002
            type[events.Event],
            list[EventCallback[events.Event]],
        ] = defaultdict(list)

    async def start(self, oauth: str, intents: datatypes.Intents) -> None:
        """
        Start the client.

        This call will never return.

        Args:
            oauth (str): The discord token
            intents (datatypes.Intents): The discord intents to use
        """
        headers = {"Authorization": oauth}
        session = aiohttp.ClientSession(headers=headers)

        self._api = Api(session)
        gateway_url = await self._api.get_gateway()
        self._gateway = Gateway(self, session)

        try:
            await self._gateway.start(gateway_url, oauth, intents)
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
        await self._gateway.close()
        await self._api.session.close()

    async def handle_event(self, event: events.Event) -> None:
        """
        Handle a incoming event.

        Args:
            event (events.Event): The event that happend.
        """
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
