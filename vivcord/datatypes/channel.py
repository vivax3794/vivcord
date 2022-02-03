"""Discord channels."""

from __future__ import annotations

from datetime import datetime
from enum import IntEnum
from typing import TYPE_CHECKING

from loguru import logger

from vivcord import helpers
from vivcord.datatypes.not_implemented import ToBeImplemented
from vivcord.datatypes.permission import Permission
from vivcord.datatypes.snowflake import Snowflake
from vivcord.datatypes.user import User

if TYPE_CHECKING:
    from vivcord import _typed_dicts as type_dicts
    from vivcord.client import Client


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

    def __init__(self, client: Client, data: type_dicts.ChannelData) -> None:
        """
        Construct channel instance.

        Args:
            client (Client): Vivcord client
            data (type_dicts.ChannelData): channel json data
        """
        self._client = client
        self._raw_data = data

        self.id_ = Snowflake(data["id"])
        self.type_ = ChannelType(data["type"])

    @staticmethod
    def parse_channel(client: Client, data: type_dicts.ChannelData) -> Channel:
        """
        Create channel from data.

        Args:
            client (Client): Vivcord client
            data (type_dicts.ChannelData): channel json

        Raises:
            ValueError: Unknown channel type

        Returns:
            Channel: Parsed channel
        """
        logger.debug(f"creating channel with data: {data!r}")
        match data["type"]:
            case 0:
                channel_type = GuildTextChannel
            case 1:
                channel_type = DMChannel
            case 2:
                channel_type = GuildVoiceChannel
            case 3:
                channel_type = GroupDMChannel
            case 4:
                channel_type = GuildCategoryChannel
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

        return channel_type(client, data)


class TextChannel(Channel):
    """A channel that handels text."""

    def __init__(self, client: Client, data: type_dicts.ChannelData) -> None:
        """
        Construct text channel instance.

        Args:
            client (Client): Vivcord client
            data (type_dicts.ChannelData): channel json data
        """
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

    def __init__(self, client: Client, data: type_dicts.ChannelData) -> None:
        """
        Construct guild channel instance.

        Args:
            client (Client): Vivcord client
            data (type_dicts.ChannelData): channel json data
        """
        super().__init__(client, data)

        guild_id = helpers.check_expected_value(data.get("guild_id"), 0)
        self.guild_id = Snowflake(guild_id)

        self.position = helpers.check_expected_value(data.get("position"), -1)
        self.permission_overwrites = ToBeImplemented()
        self.name = helpers.check_expected_value(data.get("name"), "")

        perms = data.get("permissions")
        self.current_user_permissions = (
            Permission(int(perms)) if perms is not None else None
        )


class GuildCategoryChannel(GuildChannel):
    """A guild channel."""


class GuildNonGroup(GuildChannel):
    """A guild channel that is not the group type."""

    def __init__(self, client: Client, data: type_dicts.ChannelData) -> None:
        """
        Construct guild non group channel instance.

        Args:
            client (Client): Vivcord client
            data (type_dicts.ChannelData): channel json data
        """
        super().__init__(client, data)

        parent_id = helpers.check_expected_value(data.get("parent_id"), 0)
        self.parent_id = Snowflake(parent_id) if parent_id is not None else None


class GuildTextChannel(TextChannel, GuildNonGroup):
    """A guild text channel."""

    def __init__(self, client: Client, data: type_dicts.ChannelData) -> None:
        """
        Construct guild text channel instance.

        Args:
            client (Client): Vivcord client
            data (type_dicts.ChannelData): channel json data
        """
        super().__init__(client, data)

        self.topic = helpers.check_expected_value(data.get("topic"), "")
        self.nsfw = helpers.check_expected_value(data.get("nsfw"), False)
        self.slowmode_delay = data.get("rate_limit_per_user")
        self.default_auto_archive_duration = helpers.check_expected_value(
            data.get("default_auto_archive_duration"), 0
        )


class GuildVoiceChannel(GuildNonGroup):
    """Voice channel."""

    def __init__(self, client: Client, data: type_dicts.ChannelData) -> None:
        """
        Construct guild voice channel instance.

        Args:
            client (Client): Vivcord client
            data (type_dicts.ChannelData): channel json data
        """
        super().__init__(client, data)

        self.bitrate = helpers.check_expected_value(data.get("bitrate"), 0)
        self.user_limit = helpers.check_expected_value(data.get("user_limit"), 0)
        self.rtc_region = data.get("rtc_regeion")
        self.video_quality_mode = helpers.check_expected_value(
            data.get("video_quality_mode"), 1
        )


class DMChannel(TextChannel):
    """A dm."""

    def __init__(self, client: Client, data: type_dicts.ChannelData) -> None:
        """
        Construct dm channel instance.

        Args:
            client (Client): Vivcord client
            data (type_dicts.ChannelData): channel json data
        """
        super().__init__(client, data)

        recps = helpers.check_expected_value(data.get("recipients"), None)
        if recps is None:
            self.recpients = []
        else:
            self.recpients = [User(client, recp) for recp in recps]


class GroupDMChannel(DMChannel):
    """A dm with multiple people."""

    def __init__(self, client: Client, data: type_dicts.ChannelData) -> None:
        """
        Construct group dm channel instance.

        Args:
            client (Client): Vivcord client
            data (type_dicts.ChannelData): channel json data
        """
        super().__init__(client, data)

        self.owner_id = helpers.check_expected_value(data.get("owner_id"), 0)
        self.application_id = data.get("application_id")
