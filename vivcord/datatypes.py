"""Representation of discord values."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import _internal_types as internal
    from .client import Client

# https://discord.com/developers/docs/reference#convert-snowflake-to-datetime
DISCORD_EPOCH = 1420070400000


# https://discord.com/developers/docs/topics/gateway#gateway-intents
@dataclass
class Intents:
    """Intents describes what values should be passed from discord."""

    guilds: bool = False
    guild_members: bool = False
    guild_bans: bool = False
    guild_emojis_and_stickers: bool = False
    guild_integrations: bool = False
    guild_webhooks: bool = False
    guild_invites: bool = False
    guild_voice_states: bool = False
    guild_presences: bool = False
    guild_messages: bool = False
    guild_message_reactions: bool = False
    guild_message_typing: bool = False
    direct_message: bool = False
    direct_message_reactions: bool = False
    direct_message_typing: bool = False
    guild_scheduled_events: bool = False

    def calculate_value(self) -> int:
        """
        Convert intents to int so it can be sent to discord.

        Returns:
            int: Resulting int
        """
        value = 0
        value |= self.guilds << 0
        value |= self.guild_members << 1
        value |= self.guild_bans << 2
        value |= self.guild_emojis_and_stickers << 3
        value |= self.guild_integrations << 4
        value |= self.guild_webhooks << 5
        value |= self.guild_invites << 6
        value |= self.guild_voice_states << 7
        value |= self.guild_presences << 8
        value |= self.guild_messages << 9
        value |= self.guild_message_reactions << 10
        value |= self.guild_message_typing << 11
        value |= self.direct_message << 12
        value |= self.direct_message_reactions << 13
        value |= self.direct_message_typing << 14
        value |= self.guild_scheduled_events << 16
        return value


# https://discord.com/developers/docs/reference#snowflakes
class Snowflake:
    """A discord id."""

    def __init__(self, snowflake_id: int | str) -> None:
        """
        Parse snowflake data from id.

        Args:
            snowflake_id (int): Id to get data from
        """
        snowflake_id = int(snowflake_id)

        self._raw_id = snowflake_id

        self.timestamp = datetime.fromtimestamp(
            ((snowflake_id >> 22) + DISCORD_EPOCH) / 1000
        )
        self.internal_worker_id = (snowflake_id & 0x3E0000) >> 17
        self.internal_process_id = (snowflake_id & 0x1F000) >> 12
        self.increment = snowflake_id & 0xFFF

    @classmethod
    def from_timestamp(cls, timestamp: int) -> Snowflake:
        """
        Create a snowflake from a unix timestamp.

        Args:
            timestamp (int): timestamp to create from

        Returns:
            Snowflake: Resulting snowflake
        """
        return cls((timestamp - DISCORD_EPOCH) << 22)

    def __str__(self) -> str:
        return str(self._raw_id)

    def __repr__(self) -> str:
        return f"Snowflake({self._raw_id})"

    def __int__(self) -> int:
        return self._raw_id


# https://discord.com/developers/docs/resources/user#user-object-user-flags
class UserFlags:
    """Discord user flags."""

    def __init__(self, flags: int) -> None:
        """
        Construct a flags instance.

        Args:
            flags (int): The user flags encoded as a int.
        """
        self._raw_flag = flags

        self.staff = bool(flags & (1 << 0))
        self.partner = bool(flags & (1 << 1))
        self.hypesquad = bool(flags & (1 << 2))
        self.bug_hunter_level_1 = bool(flags & (1 << 3))
        self.hypersquad_online_house_1 = bool(flags & (1 << 6))
        self.hypersquad_online_house_2 = bool(flags & (1 << 7))
        self.hypersquad_online_house_3 = bool(flags & (1 << 8))
        self.premium_early_supporter = bool(flags & (1 << 9))
        self.team_pseudo_user = bool(flags & (1 << 10))
        self.bug_hunter_level_2 = bool(flags & (1 << 14))
        self.partner = bool(flags & (1 << 15))
        self.verified_bot = bool(flags & (1 << 16))
        self.verified_developer = bool(flags & (1 << 17))
        self.certified_moderator = bool(flags & (1 << 18))
        self.bot_http_interactions = bool(flags & (1 << 19))

    def __str__(self) -> str:
        return str(self._raw_flag)

    def __repr__(self) -> str:
        return f"UserFlags({self._raw_flag})"

    def __int__(self) -> int:
        return self._raw_flag


# https://discord.com/developers/docs/resources/user#user-object-premium-types
class NitroType(IntEnum):
    """The users nitro type."""

    Nothing = 0
    Classic = 1
    Nitro = 2


# https://discord.com/developers/docs/resources/user#user-object-user-structure
class User:
    """Reperesents a user."""

    def __init__(self, client: Client, data: internal.UserData) -> None:
        """
        Construct a User instance.

        You should not construct this yourself.

        Args:
            client (Client): Discord client
            data (internal.UserData): The raw user data
        """
        self._client = client

        self.id_ = Snowflake(data["id"])
        self.username = data["username"]
        self.discriminator = data["discriminator"]

        self.bot = data.get("bot", False)
        self.system = data.get("system", False)
        self.mfa_enabled = data.get("mfa_enabled", False)
        self.premium_type = (
            NitroType(data["premium_type"]) if "premium_type" in data else None
        )

        self._avatar_hash = data["avatar"]
        self._banner_hash = data.get("banner")
        self.accent_color = data.get("accent_color")

        self.locale = data.get("locale")
        self.verified = data.get("verified")
        self.email = data.get("email")

        self.flags = UserFlags(data["public_flags"]) if "public_flags" in data else None
        self.private_flags = UserFlags(data["flags"]) if "flags" in data else None


class Guild:
    # TODO:
    pass


class Member:
    # TODO:
    pass


class ChannelType(IntEnum):
    # TODO:
    IDK = 1


class Channel:
    # TODO:
    pass


class Message:
    # TODO:
    pass


class Role:
    # TODO:
    pass


class Application:
    """A discord application."""

    def __init__(self, client: Client, data: internal.ApplicationData) -> None:
        """
        Create application instance.

        Args:
            client (Client): Discord client
            data (internal.ApplicationData): Data from discord
        """
        self.id_ = Snowflake(data["id"])
        self.owner = User(client, data["owner"]) if "owner" in data else None
        # TODO: more of this
