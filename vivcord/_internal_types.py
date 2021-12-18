from __future__ import annotations

from typing import TYPE_CHECKING, Literal, TypedDict

if TYPE_CHECKING:
    from typing import Any, TypeAlias


# https://discord.com/developers/docs/reference#error-messages
class ErrorData(TypedDict):
    """Data for a discord error."""

    code: str
    message: str


class ErrorList(TypedDict):
    """List of discord errors."""

    _errors: list[ErrorData]


ERROR_PATH: TypeAlias = ErrorList | dict[str, "ERROR_PATH"]


class ErrorResponse(TypedDict):
    """Direct error response."""

    code: int
    errors: ERROR_PATH
    message: str


# https://discord.com/developers/docs/resources/user#user-object-user-structure
class _UserDataBase(TypedDict):
    """Base for user data from discord."""

    id: int  # noqa: A003
    username: str
    discriminator: str
    avatar: str | None


class UserData(_UserDataBase, total=False):
    """User data from discord."""

    bot: bool
    system: bool
    mfa_enabled: bool
    banner: str | None
    accent_color: int | None
    locale: str
    verified: bool
    email: bool
    flags: int
    premium_type: int
    public_flags: int


class _MemberDataBase(TypedDict):
    """Member data from discord"""

    roles: list[int]
    deaf: bool
    mute: bool
    pending: bool
    permissions: str


class RoleTagData(TypedDict, total=False):
    """Role tag data from discord."""

    bot_id: int
    integration_id: int
    premium_subscriber_: None


class MemberData(_MemberDataBase, total=False):
    """Member data from discord"""

    user: UserData
    nick: str | None
    avatar: str | None
    joined_at: str
    premium_since: str | None


class _RoleDataBase(TypedDict):
    """Role data from discord."""

    id: int
    name: str
    color: int
    hoist: bool
    position: int
    permissions: str
    managed: bool
    mentionable: bool


class RoleData(_RoleDataBase, total=False):
    """Role data from discord."""

    icon: str | None
    unicode_emoji: str | None
    tags: RoleTagData


class _ChannelDataBase(TypedDict):
    """Channel data from discord."""

    id: int
    type: int


class ChannelData(_ChannelDataBase, total=False):
    """Channel data from discord."""

    guild_id: int
    position: int
    permission_overwrites: list[PermissionOverwriteData]
    name: str
    topic: str | None
    nsfw: bool
    last_message_id: int | None
    bitrate: int
    user_limit: int
    rate_limit_per_user: int
    recipients: list[UserData]
    icon: str | None
    owner_id: int
    application_id: int
    parent_id: int | None
    last_pin_timestamp: str | None
    rtc_regeion: str | None
    video_quality_mode: int
    message_count: int
    member_count: int
    thread_metadate: ThreadMetadataData
    member: ThreadMemberData
    default_audio_archive_duration: int
    permissions: str


class PermissionOverwriteData(TypedDict):
    """Permission overwrites from discord."""

    id: int
    type: int
    allow: str
    deny: str


class _ThreadMetadataDataBase(TypedDict):
    """Thread metadata from discord."""

    archived: bool
    auto_archive_duration: int
    archive_timestamp: str
    locked: bool


class ThreadMetadataData(_ThreadMetadataDataBase, total=False):
    """Thread metadata from discord."""

    invitable: bool


class _ThreadMemberDataBase(TypedDict):
    """Thread member data from discord."""

    join_timestamp: str
    flags: int


class ThreadMemberData(_ThreadMemberDataBase, total=False):
    """Thread member data from discord."""

    id: int
    user_id: int


class _MessageDataBase(TypedDict):
    """Message data from discord."""

    id: int
    channel_id: int
    author: UserData
    content: str
    timestamp: str
    edited_timestamp: str | None
    tts: bool
    mention_everyone: bool
    mentions: list[UserData]
    mention_roles: list[int]
    attachments: list[AttachmentData]
    embeds: list[EmbedData]
    pinned: bool
    type: int


class MessageData(_MessageDataBase, total=False):
    """Message data from discord."""

    member: MemberData
    mention_channels: list[ChannelMentionData]
    reactions: list[ReactionData]
    nonce: int | str
    webhook_id: int
    activity: MessageActivityData
    application: ApplicationData
    application_id: int
    message_reference: MessageReferenceData
    flags: int
    referenced_message: MemberData | None
    interaction: MessageInteractionData
    thread: ChannelData
    components: list[ComponentData]
    sticker_items: list[StickerItemData]
    stickers: list[StickerData]


class ChannelMentionData(TypedDict):
    """Channel mention from discord."""

    id: int
    guild_id: int
    type: int
    name: str


class _AttachmentDataBase(TypedDict):
    """Attachment from discord."""

    id: int
    filename: str
    size: int
    url: str
    proxy_url: str


class AttachmentData(_AttachmentDataBase, total=False):
    """Attachment from discord."""

    description: str
    content_type: str
    height: int | None
    width: int | None
    ephemeral: bool


class EmbedData(TypedDict, total=False):
    """Embed data."""

    # TODO: JUST NO! NOT TODAY


class ReactionData(TypedDict):
    """Discord reaction."""

    count: int
    me: bool
    emoji: EmojiData


class EmojiData(TypedDict):
    "Emoji data."
    # TODO: make it stop


class _MessageActivityDataBase(TypedDict):
    """Message activity."""

    type: int


class MessageActivityData(_MessageActivityDataBase, total=False):
    """Message activity."""

    party_id: str


class MessageReferenceData(TypedDict, total=False):
    """Message reference."""

    message_id: int
    channel_id: int
    guild_id: int
    fail_if_not_exists: bool


class MessageInteractionData(TypedDict):
    """Message Interaction."""

    id: int
    type: int
    name: str
    user: UserData


class ComponentData(TypedDict):
    """Component."""

    # TODO: Just no


class StickerItemData(TypedDict):
    "Sticker item."
    id: int
    name: str
    format_type: int


class StickerData(TypedDict):
    """Sticker data."""

    # TODO: I really need to sleep


# https://discord.com/developers/docs/resources/application#application-object
# TODO: most of this
class GatewayResponse(TypedDict):
    """Gateway response."""

    op: int
    d: dict[str, Any]
    s: int | None
    t: str | None


class _ApplicationDataBase(TypedDict):
    """Data about he bots application."""

    id: int  # noqa: A003


class ApplicationData(_ApplicationDataBase, total=False):
    """Data about he bots application."""

    owner: UserData


# https://discord.com/developers/docs/topics/gateway#hello-hello-structure
class HelloEventData(TypedDict):
    """Data for the hello event."""

    heartbeat_interval: int


# https://discord.com/developers/docs/topics/gateway#ready
class ReadyEventData(TypedDict):
    """Data for the ready event."""

    v: int
    user: UserData
    guilds: list[object]  # we dont use this
    session_id: str
    application: ApplicationData

    # TODO: shard


# https://discord.com/developers/docs/interactions/application-commands#application-command-object
class _CommandStructureBase(TypedDict):
    """Application command structure."""

    name: str
    description: str


class CommandStructure(_CommandStructureBase, total=False):
    """Application command structure."""

    type: int  # noqa: A003
    options: list[CommandOption]
    default_permission: bool


# https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
class _CommandOptionBase(TypedDict):
    """Slash command options."""

    type: int  # noqa: A003
    name: str
    description: str


class CommandOption(_CommandOptionBase, total=False):
    """Slash command options."""

    required: bool
    choices: list[CommandChoice]
    options: list[CommandOption]
    channel_types: list[int]
    min_value: int | float
    max_value: int | float
    autocomplete: bool


# https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-choice-structure
class CommandChoice(TypedDict):
    """A possible choice for a command Option."""

    name: str
    value: str | int | float


class _InteractionEventDataBase(TypedDict):
    """Interaction Event Data."""

    id: int  # noqa: A003
    application_id: int
    type: int
    token: str
    version: Literal[1]


class InteractionEventData(_InteractionEventDataBase, total=False):
    """Interaction Event Data."""

    data: InteractionData
    guild_id: int
    channel_id: int
    member: MemberData
    user: UserData
    message: MessageData


class _InteractionDataBase(TypedDict):
    """Interaction Data."""

    id: str  # noqa: A003
    name: str
    type: int


class InteractionData(_InteractionDataBase, total=False):
    """Interaction Data."""

    resolved: ResolvedData
    options: list[CommandOptionResult]
    custom_id: str
    component_type: int
    values: list[SelectOptionValue]
    target_id: int


class ResolvedData(TypedDict, total=False):
    """Mapping of ids to objects."""

    users: dict[int, UserData]
    members: dict[int, MemberData]
    roles: dict[int, RoleData]
    channels: dict[int, ChannelData]
    messages: dict[int, MessageData]


class _CommandOptionResultBase(TypedDict):
    """Options select in interaction."""

    name: str
    type: int


class CommandOptionResult(_CommandOptionResultBase, total=False):
    """Options select in interaction."""

    value: str | int | float
    focused: bool


class SelectOptionValue:
    """Select option."""

    # TODO: idk anymore
