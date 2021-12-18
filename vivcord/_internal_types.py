from __future__ import annotations

from typing import TYPE_CHECKING, List, Literal, TypedDict

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


class MemberData(_MemberDataBase, total=False):
    """Member data from discord"""

    user: UserData
    nick: str | None
    avatar: str | None
    joined_at: str
    premium_since: str | None


class RoleTagData(TypedDict, total=False):
    """Role tag data from discord."""

    bot_id: int
    integration_id: int
    premium_subscriber_: None


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


# https://discord.com/developers/docs/resources/channel#embed-object-embed-structure
class EmbedData(TypedDict, total=False):
    """Embed data."""

    title: str
    type: str
    description: str
    url: str
    timestamp: str
    color: int
    footer: EmbedFooterData
    image: EmbedImageData
    thumbnail: EmbedThumbnailData
    video: EmbedVideoData
    provider: EmbedProviderData
    author: EmbedAuthorData
    fields: list[EmbedFieldData]


# https://discord.com/developers/docs/resources/channel#embed-object-embed-thumbnail-structure
class _EmbedThumbnailDataBase(TypedDict):
    """Embed thumbnail."""

    url: str


class EmbedThumbnailData(_EmbedThumbnailDataBase, total=False):
    """Embed thumbnail."""

    proxy_url: str
    height: int
    width: int


# https://discord.com/developers/docs/resources/channel#embed-object-embed-video-structure
class EmbedVideoData(TypedDict, total=False):
    """Embed video data."""

    url: str
    proxy_url: str
    height: int
    width: int


# https://discord.com/developers/docs/resources/channel#embed-object-embed-image-structure
class _EmbedImageDataBase(TypedDict):
    """Embed image."""

    url: str


class EmbedImageData(_EmbedImageDataBase, total=False):
    """Embed image."""

    proxy_url: str
    height: int
    width: int


# https://discord.com/developers/docs/resources/channel#embed-object-embed-provider-structure
class EmbedProviderData(TypedDict, total=False):
    """Embed provider."""

    name: str
    url: str


# https://discord.com/developers/docs/resources/channel#embed-object-embed-author-structure
class _EmbedAuthorDataBase(TypedDict):
    """Embed Author"""

    name: str


class EmbedAuthorData(_EmbedAuthorDataBase, total=False):
    """Embed Author"""

    url: str
    icon_url: str
    proxy_icon_url: str


# https://discord.com/developers/docs/resources/channel#embed-object-embed-footer-structure
class _EmbedFooterDataBase(TypedDict):
    """Embeed footer"""

    text: str


class EmbedFooterData(_EmbedFooterDataBase, total=False):
    """Embeed footer"""

    icon_url: str
    proxy_icon_url: str


# https://discord.com/developers/docs/resources/channel#embed-object-embed-field-structure
class _EmbedFieldDataBase(TypedDict):
    """Embed field."""

    name: str
    value: str


class EmbedFieldData(_EmbedFieldDataBase, total=False):
    """Embed field."""

    inline: bool


class ReactionData(TypedDict):
    """Discord reaction."""

    count: int
    me: bool
    emoji: EmojiData


class _EmojiDataBase(TypedDict):
    """Emoji data."""

    id: int | None
    name: str | None


class EmojiData(_EmojiDataBase, total=False):
    """Emoji data."""

    roles: list[int]
    user: UserData
    require_colons: bool
    managed: bool
    animated: bool
    available: bool


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


# https://discord.com/developers/docs/interactions/message-components#component-object-component-structure
class _ComponentDataBase(TypedDict):
    """Discord component data."""

    type: int


class ComponentData(_ComponentDataBase, total=False):
    """Discord component data."""

    custom_id: str
    disabled: bool
    style: int
    label: str
    emoji: EmojiData
    url: str
    options: list[SelectOptionData]
    placeholder: str
    min_values: int
    max_value: int
    components: list[ComponentData]


# https://discord.com/developers/docs/interactions/message-components#select-menu-object-select-option-structure
class _SelectOptionDataBase(TypedDict):
    """Select option."""

    label: str
    value: str


class SelectOptionData(_SelectOptionDataBase, total=False):
    """Select option."""

    description: str
    emoji: EmojiData
    default: bool


# https://discord.com/developers/docs/resources/sticker#sticker-item-object-sticker-item-structure
class StickerItemData(TypedDict):
    "Sticker item."
    id: int
    name: str
    format_type: int


# https://discord.com/developers/docs/resources/sticker#sticker-object-sticker-structure
class _StickerDataBase(TypedDict):
    """Sticker data."""

    id: int
    name: str
    description: str | None
    tags: str
    asset: Literal[""]
    type: int
    format_type: int


class StickerData(_StickerDataBase, total=False):
    """Sticker data."""

    pack_id: int
    available: bool
    guild_id: int
    user: UserData
    sort_value: int


# https://discord.com/developers/docs/resources/guild#guild-object-guild-structure
class _GuildDataBase(TypedDict):
    """Discord server (guild)."""

    id: int
    name: str
    icon: str | None
    splash: str | None
    discovery_splash: str | None
    owner_id: int
    afk_channel_id: int | None
    afk_timeout: int
    verification_level: int
    default_message_notifications: int
    explicit_content_filter: int
    roles: list[RoleData]
    emojis: list[EmojiData]
    features: list[str]
    mfa_level: int
    application_id: int | None
    system_channel_id: int | None
    system_channel_flags: int
    rules_channel_id: int | None
    vanity_url_code: str | None
    description: str | None
    banner: str | None
    premium_tier: int
    preferred_locale: str
    public_updates_channel_id: int | None
    nsfw_level: int
    premium_progress_bar_enabled: bool


class GuildData(_GuildDataBase, total=False):
    """Discord server (guild)."""

    icon_hash: str | None
    owner: bool
    permissions: str
    widget_enabled: bool
    widget_channel_id: int | None
    joined_at: str
    large: bool
    unavailable: bool
    member_count: int
    voice_states: list[VoiceStateData]
    members: list[MemberData]
    channels: list[ChannelData]
    threads: list[ChannelData]
    presences: list[PresenceUpdateData]
    max_presences: int | None
    max_members: int
    premium_subscription_count: int
    max_video_channel_users: int
    approximate_member_count: int
    approximate_presence_count: int
    welcome_screen: WelcomeScreenData
    stage_instances: list[StageInstanceData]
    stickers: list[StickerData]
    guild_scheduled_events: list[GuildScheduledEventData]


# https://discord.com/developers/docs/resources/voice#voice-state-object-voice-state-structure
class _VoiceStateDataBase(TypedDict):
    """Voice state."""

    channel_id: int | None
    user_id: int
    session_id: str
    deaf: bool
    mute: bool
    self_dead: bool
    self_mute: bool
    self_video: bool
    suppres: bool
    request_to_speak_timestamp: str | None


class VoiceStateData(_VoiceStateDataBase, total=False):
    """Voice state."""

    guild_id: int
    member: MemberData


# https://discord.com/developers/docs/topics/gateway#presence-update-presence-update-event-fields
class PresenceUpdateData(TypedDict):
    """Presence update."""

    user: UserData
    guild_id: int
    status: str
    activities: list[ActivityData]
    client_status: ClientStatusData


# https://discord.com/developers/docs/topics/gateway#activity-object-activity-structure
class _ActivityDataBase(TypedDict):
    """Activity."""

    name: str
    type: int
    created_at: int


class ActivityData(_ActivityDataBase, total=False):
    """Activity."""

    url: str | None
    timestamps: list[TimestampData]
    application_id: int
    details: str | None
    state: str | None
    emoji: EmojiData | None
    party: PartyData
    assets: AssetData
    secrets: ActivitySecretData
    instance: bool
    flags: int
    buttons: list[str]


class TimestampData(TypedDict, total=False):
    """Activity timestamp."""

    start: int
    end: int


class PartyData(TypedDict, total=False):
    """Activity part."""

    id: str
    size: list[int]


class AssetData(TypedDict, total=False):
    """Activity asset data."""

    large_image: str
    large_text: str
    small_image: str
    small_text: str


class ActivitySecretData(TypedDict, total=False):
    """Activity secret data."""

    join: str
    spectate: str
    match: str


class ClientStatusData(TypedDict, total=False):
    """Client status."""

    desktop: str
    mobile: str
    web: str


class WelcomeScreenData(TypedDict):
    """Welcome screen."""

    description: str | None
    welcome_channels: list[WelcomeChannelData]


class WelcomeChannelData(TypedDict):
    """Welcome channel."""

    channel_id: int
    description: str
    emoji_id: int | None
    emoji_name: str | None


class StageInstanceData(TypedDict):
    """Stage instance."""

    id: int
    guild_id: int
    channel_id: int
    topic: str
    privacy_level: int
    discoverable_disabled: bool


class _GuildScheduledEventDataBase(TypedDict):
    """Guild scheduled event."""

    id: int
    guild_id: int
    channel_id: int | None
    creator_id: int | None
    name: str
    scheduled_start_time: str
    scheduled_end_time: str | None
    privacy_level: int
    status: int
    entity_type: int
    entity_id: int | None
    entity_metadata: EntityMetadata | None


class GuildScheduledEventData(_GuildScheduledEventDataBase, total=False):
    """Guild scheduled event."""

    description: str
    creator: UserData
    user_count: int


class EntityMetadata(TypedDict, total=False):
    """Entity metadata."""

    location: str


# https://discord.com/developers/docs/resources/application#application-object
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
    guilds: list[GuildData]  # we dont use this
    session_id: str
    application: ApplicationData


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
