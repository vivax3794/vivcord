"""Most datetypes created by the library."""

from __future__ import annotations

__all__ = (
    "Embed",
    "embed",
    "Intents",
    "Permission",
    "Snowflake",
    "User",
    "Member",
    "Guild",
    "channel",
    "Channel",
    "Message",
    "SendMessageData",
    "Role",
    "Application",
)

from typing import TYPE_CHECKING

from vivcord.datatypes import channel, embed
from vivcord.datatypes.channel import Channel
from vivcord.datatypes.embed import Embed
from vivcord.datatypes.guild import Guild
from vivcord.datatypes.intents import Intents
from vivcord.datatypes.message import Message, SendMessageData
from vivcord.datatypes.permission import Permission
from vivcord.datatypes.role import Role
from vivcord.datatypes.snowflake import Snowflake
from vivcord.datatypes.user import Member, User

if TYPE_CHECKING:
    from vivcord import _typed_dicts as type_dicts
    from vivcord.client import Client


class Application:
    """A discord application."""

    def __init__(self, client: Client, data: type_dicts.ApplicationData) -> None:
        """
        Create application instance.

        Args:
            client (Client): Discord client
            data (type_dicts.ApplicationData): Data from discord
        """
        self.id_ = Snowflake(data["id"])
        self.owner = User(client, data["owner"]) if "owner" in data else None
