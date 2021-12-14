"""Discord events."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from loguru import logger

from . import datatypes

if TYPE_CHECKING:
    from typing import Any, Callable

    from . import _internal_types as internal


EventT = TypeVar("EventT", bound="Event")


class EventMapManager:
    """Class for managing discord opcode/type to library classes."""

    def __init__(self) -> None:
        """Create event mapper."""
        self.opcodes: dict[int, type[Event]] = {}
        self.types: dict[str, type[Event]] = {}

    def register_op(self, op: int) -> Callable[[type[EventT]], type[EventT]]:
        """
        Register a new class using the provided opcode.

        Args:
            op (int): Opcode to register under

        Returns:
            Callable[[type[EventT]], type[EventT]]: Decorator that can be used on class to register it
        """

        def decorator(event_type: type[EventT]) -> type[EventT]:
            self.opcodes[op] = event_type
            return event_type

        return decorator

    def register_type(self, type_: str) -> Callable[[type[EventT]], type[EventT]]:
        """
        Register a new class using the provided type ("t" key from discord).

        Args:
            type_ (str): type to register under

        Returns:
            Callable[[type[EventT]], type[EventT]]: Decorator that can be used on class to register it
        """

        def decorator(event_type: type[EventT]) -> type[EventT]:
            self.types[type_] = event_type
            return event_type

        return decorator

    def get_type(self, op: int, type_: str | None) -> type[Event]:
        """
        Get the Event type based on op and type_.

        Defaults to Event if not found

        Args:
            op (int): opcode to lookup
            type_ (str): type to lookup (used when op == 0)

        Returns:
            type[Event]: The event type that should be used
        """
        if op == 0 and type_ is not None:
            return self.types.get(type_, Event)
        else:
            return self.opcodes.get(op, Event)


event_map_manager = EventMapManager()


class Event:
    """Discord event."""

    def __init__(self, data: dict[str, Any]) -> None:
        """
        Create default event.

        Prints a warning as this type should not be used directly.

        Args:
            data (dict[str, Any]): data to be used
        """
        if self.__class__ == Event:
            logger.warning(f"unknown event: {data!r}")


# https://discord.com/developers/docs/topics/gateway#hello-hello-structure
@event_map_manager.register_op(10)
class Hello(Event):
    """The gateway hello event."""

    def __init__(self, data: internal.HelloEventData) -> None:
        """
        Create hello event.

        Args:
            data (dict[str, Any]): data to be used
        """
        self.heartbeat_interval = data["heartbeat_interval"]

    heartbeat_interval: int


# https://discord.com/developers/docs/topics/gateway#heartbeating-example-gateway-heartbeat-ack
@event_map_manager.register_op(11)
class HearthbeatACK(Event):
    """Hearthbeat acknowledgement."""


# https://discord.com/developers/docs/topics/gateway#ready
@event_map_manager.register_type("READY")
class Ready(Event):
    """event sent when gateway is ready."""

    def __init__(self, data: internal.ReadyEventData) -> None:
        """
        Create ready event.

        Args:
            data (dict[str, Any]): data to be used
        """
        self.version = data["v"]
        self.user = datatypes.User(data["user"])
        self.application = datatypes.Application(data["application"])
        # Todo: more of this
