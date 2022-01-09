"""Representation of discord values."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum
from typing import TYPE_CHECKING

from loguru import logger

from . import _internal_types as internal
from . import helpers

if TYPE_CHECKING:
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
        value |= self.guild_scheduled_events << 16
        return value


class Permission:
    """Discord permissions."""

    def __init__(self, permissions_int: int) -> None:
        """Parse individual permissions out of the permissions int."""
        self.create_instant_invite = (permissions_int & (2 ^ 0)) != 0
        self.kick_members = (permissions_int & (2 ^ 1)) != 0
        self.ban_members = (permissions_int & (2 ^ 2)) != 0
        self.administrator = (permissions_int & (2 ^ 3)) != 0
        self.manage_channels = (permissions_int & (2 ^ 4)) != 0
        self.manage_guild = (permissions_int & (2 ^ 5)) != 0
        self.add_reactions = (permissions_int & (2 ^ 6)) != 0
        self.view_audit_log = (permissions_int & (2 ^ 7)) != 0
        self.priority_speaker = (permissions_int & (2 ^ 8)) != 0
        self.stream = (permissions_int & (2 ^ 9)) != 0
        self.view_channel = (permissions_int & (2 ^ 10)) != 0
        self.send_messages = (permissions_int & (2 ^ 11)) != 0
        self.send_tts_messages = (permissions_int & (2 ^ 12)) != 0
        self.manage_messages = (permissions_int & (2 ^ 13)) != 0
        self.embed_links = (permissions_int & (2 ^ 14)) != 0
        self.attach_files = (permissions_int & (2 ^ 15)) != 0
        self.read_message_history = (permissions_int & (2 ^ 16)) != 0
        self.mention_everyone = (permissions_int & (2 ^ 17)) != 0
        self.use_external_emojies = (permissions_int & (2 ^ 18)) != 0
        self.view_guild_insights = (permissions_int & (2 ^ 19)) != 0
        self.connect = (permissions_int & (2 ^ 20)) != 0
        self.speak = (permissions_int & (2 ^ 21)) != 0
        self.mute_members = (permissions_int & (2 ^ 22)) != 0
        self.deafen_members = (permissions_int & (2 ^ 23)) != 0
        self.move_members = (permissions_int & (2 ^ 24)) != 0
        self.use_vad = (permissions_int & (2 ^ 25)) != 0
        self.change_nickname = (permissions_int & (2 ^ 26)) != 0
        self.manage_nicknames = (permissions_int & (2 ^ 27)) != 0
        self.manage_roles = (permissions_int & (2 ^ 28)) != 0
        self.manage_webhooks = (permissions_int & (2 ^ 29)) != 0
        self.manage_emojis_and_stickers = (permissions_int & (2 ^ 30)) != 0
        self.use_application_commands = (permissions_int & (2 ^ 31)) != 0
        self.request_to_speak = (permissions_int & (2 ^ 32)) != 0
        self.manage_events = (permissions_int & (2 ^ 33)) != 0
        self.manage_threads = (permissions_int & (2 ^ 34)) != 0
        self.create_public_threads = (permissions_int & (2 ^ 35)) != 0
        self.create_private_threads = (permissions_int & (2 ^ 36)) != 0
        self.use_external_stickers = (permissions_int & (2 ^ 37)) != 0
        self.send_messages_in_threads = (permissions_int & (2 ^ 38)) != 0
        self.start_embed_activities = (permissions_int & (2 ^ 39)) != 0
        self.moderate_members = (permissions_int & (2 ^ 40)) != 0

    def calculate_value(self) -> int:
        """Convert back to int."""
        value = 0
        value |= self.create_instant_invite << 0
        value |= self.kick_members << 1
        value |= self.ban_members << 2
        value |= self.administrator << 3
        value |= self.manage_channels << 4
        value |= self.manage_guild << 5
        value |= self.add_reactions << 6
        value |= self.view_audit_log << 7
        value |= self.priority_speaker << 8
        value |= self.stream << 9
        value |= self.view_channel << 10
        value |= self.send_messages << 11
        value |= self.send_tts_messages << 12
        value |= self.manage_messages << 13
        value |= self.embed_links << 14
        value |= self.attach_files << 15
        value |= self.read_message_history << 16
        value |= self.mention_everyone << 17
        value |= self.use_external_emojies << 18
        value |= self.view_guild_insights << 19
        value |= self.connect << 20
        value |= self.speak << 21
        value |= self.mute_members << 22
        value |= self.deafen_members << 23
        value |= self.move_members << 24
        value |= self.use_vad << 25
        value |= self.change_nickname << 26
        value |= self.manage_nicknames << 27
        value |= self.manage_roles << 28
        value |= self.manage_webhooks << 29
        value |= self.manage_emojis_and_stickers << 30
        value |= self.use_application_commands << 31
        value |= self.request_to_speak << 32
        value |= self.manage_events << 33
        value |= self.manage_threads << 34
        value |= self.create_public_threads << 35
        value |= self.create_private_threads << 36
        value |= self.use_external_stickers << 37
        value |= self.send_messages_in_threads << 38
        value |= self.start_embed_activities << 39
        value |= self.moderate_members << 40
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
        self._raw_data = data

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
    """A discord server."""


# https://discord.com/developers/docs/resources/guild#guild-member-object
class Member:
    """Discord member."""

    def __init__(self, client: Client, data: internal.MemberData) -> None:
        """Construct guild instance."""
        self._client = client
        self._raw_data = data

        self.role_ids = [Snowflake(id_) for id_ in data["roles"]]
        self.joined_at = datetime.fromisoformat(data["joined_at"])
        self.deaf = data["deaf"]
        self.mute = data["mute"]

        self.user = User(client, data["user"]) if "user" in data else None
        self.nick = data.get("nick")
        self.avatar_hash = data.get("avatar")

        prem = data.get("fromtimestamp")
        self.premium_since = (
            datetime.fromtimestamp(int(prem)) if prem is not None else None
        )
        self.pending = data.get("pending")

        perms = data.get("permissions")
        self.permissions = Permission(int(perms)) if perms is not None else None

        timeout_time = data.get("communication_disabled_until")
        self.timeout_until = (
            datetime.fromtimestamp(int(timeout_time))
            if timeout_time is not None
            else None
        )


class ChannelType(IntEnum):
    """Discord channel type."""

    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_NEWS = 5
    GUILD_STORE = 6
    GUILD_NEWS_THREAD = 10
    GUILD_PUBLIC_THREAD = 11
    GUILD_PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13


class Channel:
    """Discord channel."""

    def __init__(self, client: Client, data: internal.ChannelData) -> None:
        """Construct channel instace."""
        self._client = client
        self._raw_data = data

        self.id_ = Snowflake(data["id"])
        self.type_ = ChannelType(data["type"])

    @staticmethod
    def parse_channel(client: Client, data: internal.ChannelData) -> Channel:
        """Parse channel."""
        logger.debug(f"creating channel with data: {data!r}")
        match data["type"]:
            case 0:
                return GuildTextChannel(client, data)
            case 1:
                return DMChannel(client, data)
            case 2:
                return GuildVoiceChannel(client, data)
            case 3:
                return GroupDMChannel(client, data)
            case 4:
                return GuildCategoryChannel(client, data)
            # TODO: parse more channel types.
            # case 5:
            #     return GuildNewsChannel(client, data)
            # case 6:
            #     return GuildStoreChannel(client, data)
            # case 10:
            #     return GuildNewsThreadChannel(client, data)
            # case 11:
            #     return GuildPublicThreadChannel(client, data)
            # case 12:
            #     return GuildPrivateThreadChannel(client, data)
            # case 13:
            #     return GuildStageVoiceChannel(client, data)
            case _:
                raise ValueError(f"Unknown channel type: {data['type']}")


class TextChannel(Channel):
    """A channel that handels text."""

    def __init__(self, client: Client, data: internal.ChannelData) -> None:
        """Construct a text channel."""
        super().__init__(client, data)

        last_message_id = data.get("last_message_id")
        self.last_message_id = (
            Snowflake(last_message_id) if last_message_id is not None else None
        )

        last_pin_timestamp = data.get("last_pin_timestamp")
        self.last_pin_timestamp = (
            datetime.fromtimestamp(int(last_pin_timestamp))
            if last_pin_timestamp is not None
            else None
        )


class GuildChannel(Channel):
    """Channel in a guild."""

    def __init__(self, client: Client, data: internal.ChannelData) -> None:
        """Construct a guild channel."""
        super().__init__(client, data)

        guild_id = helpers.check_expected_value(data.get("guild_id"), 0)
        self.guild_id = Snowflake(guild_id)

        self.position = helpers.check_expected_value(data.get("position"), -1)
        self.permission_overwrites = internal.ToBeImplemented()
        self.name = helpers.check_expected_value(data.get("name"), "")

        perms = data.get("permissions")
        self.current_user_permissions = (
            Permission(int(perms)) if perms is not None else None
        )


class GuildCategoryChannel(GuildChannel):
    """A guild channel."""


class GuildNonGroup(GuildChannel):
    """A guild channel that is not the group type."""

    def __init__(self, client: Client, data: internal.ChannelData) -> None:
        """Construct a guild channel."""
        super().__init__(client, data)

        parent_id = helpers.check_expected_value(data.get("parent_id"), 0)
        self.parent_id = Snowflake(parent_id) if parent_id is not None else None


class GuildTextChannel(TextChannel, GuildNonGroup):
    """A guild text channel."""

    def __init__(self, client: Client, data: internal.ChannelData) -> None:
        """Construct a guild text channel."""
        super().__init__(client, data)

        self.topic = helpers.check_expected_value(data.get("topic"), "")
        self.nsfw = helpers.check_expected_value(data.get("nsfw"), False)
        self.slowmode_delay = data.get("rate_limit_per_user")
        self.default_auto_archive_duration = helpers.check_expected_value(
            data.get("default_auto_archive_duration"), 0
        )


class GuildVoiceChannel(GuildNonGroup):
    def __init__(self, client: Client, data: internal.ChannelData) -> None:
        super().__init__(client, data)

        self.bitrate = helpers.check_expected_value(data.get("bitrate"), 0)
        self.user_limit = helpers.check_expected_value(data.get("user_limit"), 0)
        self.rtc_region = data.get("rtc_regeion")
        self.video_quality_mode = helpers.check_expected_value(
            data.get("video_quality_mode"), 1
        )


class DMChannel(TextChannel):
    "A dm."

    def __init__(self, client: Client, data: internal.ChannelData) -> None:
        "Construct dm channel."
        super().__init__(client, data)

        recps = helpers.check_expected_value(data.get("recipients"), None)
        if recps is None:
            self.recpients = []
        else:
            self.recpients = [User(client, recp) for recp in recps]


class GroupDMChannel(DMChannel):
    """A dm with multiple people."""

    def __init__(self, client: Client, data: internal.ChannelData) -> None:
        super().__init__(client, data)

        self.owner_id = helpers.check_expected_value(data.get("owner_id"), 0)
        self.application_id = data.get("application_id")


class Message:
    # TODO:
    pass


class SendMessageData:
    def __init__(self, content: str) -> None:
        self.content = content
    
    def convert_to_dict(self) -> dict[str, str]:
        return {
            "content": self.content
        }


class Embed:
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
