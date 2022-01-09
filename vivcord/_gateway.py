"""Handle events from the discord gateway."""

# TODO: Support for resuming sessions

from __future__ import annotations

import asyncio
import random
import sys
from typing import TYPE_CHECKING, Generic, TypeVar

from loguru import logger

from . import events
from ._constants import GATEWAY_VERSION
from .events import event_map_manager

if TYPE_CHECKING:
    from typing import Any, TypeGuard

    import aiohttp

    from . import datatypes
    from ._internal_types import GatewayResponse
    from .client import Client

EventT = TypeVar("EventT", bound=events.Event)


class _EventWaiter(Generic[EventT]):
    """A class helping in waiting for an event to happen."""

    def __init__(self, event_type: type[EventT]) -> None:
        """
        Create waiter.

        Args:
            event_type (EventT): The event type to wait for
        """
        self._type = event_type
        self._event = asyncio.Event()
        self._value: EventT | None = None

    async def wait(self) -> EventT:
        """
        Wait for event to happen.

        Returns:
            EventT: The event that happend.

        Raises:
            ValueError: if the internal event is set without a value being provided.
        """
        _ = await self._event.wait()
        if self._value is None:
            raise ValueError("_event set without value being set.")
        return self._value

    def give(self, event: EventT) -> None:
        """
        Set the event and wake up anybody waiting for it.

        Args:
            event (EventT): The event that happend
        """
        self._value = event
        self._event.set()

    def is_event(self, event_type: type[EventT]) -> TypeGuard[_EventWaiter[EventT]]:
        """
        Check if this waitier if for the given event.

        Args:
            event_type (type[EventT]): The event type to check for

        Returns:
            bool: If the waiter is of the given type.
        """
        return self._type == event_type


# https://discord.com/developers/docs/topics/gateway
class Gateway:
    """Handle connection to discord gateway."""

    def __init__(self, client: Client, session: aiohttp.ClientSession):
        """
        Create a Gateway.

        Args:
            client (Client): The VivCord client this belongs to.
            session (aiohttp.ClientSession): The https session to use when connecting.
        """
        self._client = client
        self._session = session

        self._ws = None
        self._waiters: list[_EventWaiter[Any]] = []
        self._last_sequence: int | None = None

    def _parse_event(self, response: GatewayResponse) -> events.Event:
        """
        Parse json into a event instance.

        Args:
            response (GatewayResponse): The data to parse

        Returns:
            events.Event: The parsed event.
        """
        # https://discord.com/developers/docs/topics/gateway#payloads-gateway-payload-structure
        op = response["op"]
        data = response["d"]
        type_ = response["t"]
        self._last_sequence = response["s"]

        event_type = event_map_manager.get_type(op, type_)
        return event_type(self._client, data)

    async def wait_for(self, event_type: type[EventT]) -> EventT:
        """
        Wait for an event to happen.

        Args:
            event_type (events.Event): The event type to wait for.

        Returns:
            EventT: The event that happend.
        """
        waiter = _EventWaiter(event_type)
        self._waiters.append(waiter)
        # logger.debug(f"waiting for {event_type}")
        return await waiter.wait()

    async def start(self, url: str, oauth: str, intents: datatypes.Intents) -> None:
        """
        Start the gateway.

        Args:
            url (str): Url to connect to
            oauth (str): Discord bot oauth token.
            intents (datatypes.Intents): Intents to pass to discord.
        """
        # https://discord.com/developers/docs/topics/gateway#connecting-to-the-gateway
        logger.info("starting gateway")
        self._ws = await self._session.ws_connect(
            url,
            params={
                "v": str(GATEWAY_VERSION),
                "encoding": "json",
            },
        )

        self._client.task_manger.add_task(asyncio.create_task(self._read_loop()))
        logger.info("waiting for hello")
        hello = await self.wait_for(events.Hello)

        self._client.task_manger.add_task(
            asyncio.create_task(self._hearthbeat(hello.heartbeat_interval / 1000))
        )

        # https://discord.com/developers/docs/topics/gateway#identify
        logger.info("identifying")
        await self._ws.send_json(
            {
                "op": 2,
                "d": {
                    "token": oauth,
                    "properties": {
                        "$os": sys.platform,
                        "$browser": "VivCord",
                        "$device": "VivCord",
                    },
                    "intents": intents.calculate_value(),
                },
            }
        )

        _ = await self.wait_for(events.Ready)

    async def close(self) -> None:
        """
        Close the connection.

        Raises:
            ValueError: socket was not open
        """
        logger.debug("closing")

        if self._ws is None:
            raise ValueError("Socket not open.")

        _ = await self._ws.close()

    async def _read_loop(self) -> None:
        """
        Loop and read events forever.

        Raises:
            ValueError: socket was not open
        """
        if self._ws is None:
            raise ValueError("Socket not open.")

        while True:
            data = await self._ws.receive_json()
            event = self._parse_event(data)
            event_task = asyncio.create_task(self._on_event(event))
            self._client.task_manger.add_task(event_task)

    async def _hearthbeat(self, interval: float) -> None:
        """
        Send hearthbeats to keep the connection alive.

        Args:
            interval (float): How often to send a hearthbeat.

        Raises:
            ValueError: socket was not open
        """
        # https://discord.com/developers/docs/topics/gateway#heartbeating
        if self._ws is None:
            raise ValueError("Socket not open.")

        await asyncio.sleep(interval * random.random(), None)  # noqa: S311 DUO102
        while True:
            await self._ws.send_json({"op": 1, "d": self._last_sequence})
            _ = await self.wait_for(events.HearthbeatACK)
            await asyncio.sleep(interval, None)

    async def _on_event(self, event: events.Event) -> None:
        """
        Handle a event.

        Args:
            event (events.Event): The event to handle.
        """
        logger.debug(f"got event: {event}")

        # handle waiters
        for waiter in self._waiters:
            if waiter.is_event(type(event)):
                waiter.give(event)

        await self._client.handle_event(event)
