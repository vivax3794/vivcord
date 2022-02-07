from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from typing import Any, Literal, TypeAlias

    from typing_extensions import NotRequired, Required


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


class UserData(TypedDict, total=False):
    """User data from discord."""

    id: Required[int]  # noqa: A003
    username: Required[str]
    discriminator: Required[str]
    avatar: Required[str | None]

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


class MemberData(TypedDict, total=False):
    """Member data from discord."""

    roles: Required[list[int]]
    joined_at: Required[str]
    deaf: Required[bool]
    mute: Required[bool]

    user: UserData
    nick: str | None
    avatar: str | None
    premium_since: str | None
    pending: bool
    permissions: str
    communication_disabled_until: str | None


class RoleTagData(TypedDict, total=False):
    """Role tag data from discord."""

    bot_id: int
    integration_id: int
    premium_subscriber_: None


class RoleData(TypedDict):
    """Role data from discord."""

    id: int  # noqa: A003
    name: str
    color: int
    hoist: bool
    position: int
    permissions: str
    managed: bool
    mentionable: bool

    icon: NotRequired[str | None]
    unicode_emoji: NotRequired[str | None]
    tags: NotRequired[RoleTagData]


class ChannelData(TypedDict, total=False):
    """Channel data from discord."""

    id: Required[int]  # noqa: A003
    type: Required[int]  # noqa: A003

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

    id: int  # noqa: A003
    type: int  # noqa: A003
    allow: str
    deny: str


class ThreadMetadataData(TypedDict):
    """Thread metadata from discord."""

    archived: bool
    auto_archive_duration: int
    archive_timestamp: str
    locked: bool

    invitable: NotRequired[bool]


class ThreadMemberData(TypedDict, total=False):
    """Thread member data from discord."""

    join_timestamp: Required[str]
    flags: Required[int]

    id: int  # noqa: A003
    user_id: int


class MessageData(TypedDict, total=False):
    """Message data from discord."""

    id: Required[int]  # noqa: A003
    channel_id: Required[int]
    author: Required[UserData]
    content: Required[str]
    timestamp: Required[str]
    edited_timestamp: Required[str | None]
    tts: Required[bool]
    mention_everyone: Required[bool]
    mentions: Required[list[UserData]]
    mention_roles: Required[list[int]]
    attachments: Required[list[AttachmentData]]
    embeds: Required[list[EmbedData]]
    pinned: Required[bool]
    type: Required[int]  # noqa: A003

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


class SendMessageData(TypedDict, total=False):
    """Data that can be sent to discord when creating a message."""

    content: str
    embeds: list[EmbedData]


class ChannelMentionData(TypedDict):
    """Channel mention from discord."""

    id: int  # noqa: A003
    guild_id: int
    type: int  # noqa: A003
    name: str


class AttachmentData(TypedDict, total=False):
    """Attachment from discord."""

    id: Required[int]  # noqa: A003
    filename: Required[str]
    size: Required[int]
    url: Required[str]
    proxy_url: Required[str]

    description: str
    content_type: str
    height: int | None
    width: int | None
    ephemeral: bool


# https://discord.com/developers/docs/resources/channel#embed-object-embed-structure
class EmbedData(TypedDict, total=False):
    """Embed data."""

    title: str
    type: str  # noqa: A003
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
class EmbedThumbnailData(TypedDict, total=False):
    """Embed thumbnail."""

    url: Required[str]

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
class EmbedImageData(TypedDict, total=False):
    """Embed image."""

    url: Required[str]

    proxy_url: str
    height: int
    width: int


# https://discord.com/developers/docs/resources/channel#embed-object-embed-provider-structure
class EmbedProviderData(TypedDict, total=False):
    """Embed provider."""

    name: str
    url: str


# https://discord.com/developers/docs/resources/channel#embed-object-embed-author-structure
class EmbedAuthorData(TypedDict, total=False):
    """Embed Author."""

    name: Required[str]

    url: str
    icon_url: str
    proxy_icon_url: str


# https://discord.com/developers/docs/resources/channel#embed-object-embed-footer-structure
class EmbedFooterData(TypedDict, total=False):
    """Embeed footer."""

    text: Required[str]

    icon_url: str
    proxy_icon_url: str


# https://discord.com/developers/docs/resources/channel#embed-object-embed-field-structure
class EmbedFieldData(TypedDict):
    """Embed field."""

    name: str
    value: str

    inline: NotRequired[bool]


class ReactionData(TypedDict):
    """Discord reaction."""

    count: int
    me: bool
    emoji: EmojiData


class EmojiData(TypedDict):
    """Emoji data."""

    id: Required[int | None]  # noqa: A003
    name: Required[str | None]

    roles: list[int]
    user: UserData
    require_colons: bool
    managed: bool
    animated: bool
    available: bool


class MessageActivityData(TypedDict):
    """Message activity."""

    type: int  # noqa: A003
    party_id: NotRequired[str]


class MessageReferenceData(TypedDict, total=False):
    """Message reference."""

    message_id: int
    channel_id: int
    guild_id: int
    fail_if_not_exists: bool


class MessageInteractionData(TypedDict):
    """Message Interaction."""

    id: int  # noqa: A003
    type: int  # noqa: A003
    name: str
    user: UserData


# https://discord.com/developers/docs/interactions/message-components#component-object-component-structure
class ComponentData(TypedDict, total=False):
    """Discord component data."""

    type: Required[int]  # noqa: A003

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
class SelectOptionData(TypedDict, total=False):
    """Select option."""

    label: Required[str]
    value: Required[str]

    description: str
    emoji: EmojiData
    default: bool


# https://discord.com/developers/docs/resources/sticker#sticker-item-object-sticker-item-structure
class StickerItemData(TypedDict):
    """Sticker item."""

    id: int  # noqa: A003
    name: str
    format_type: int


# https://discord.com/developers/docs/resources/sticker#sticker-object-sticker-structure
class StickerData(TypedDict, total=False):
    """Sticker data."""

    id: Required[int]  # noqa: A003
    name: Required[str]
    description: Required[str | None]
    tags: Required[str]
    asset: Required[Literal[""]]
    type: Required[int]  # noqa: A003
    format_type: Required[int]

    pack_id: int
    available: bool
    guild_id: int
    user: UserData
    sort_value: int


# https://discord.com/developers/docs/resources/guild#guild-object-guild-structure
class GuildData(TypedDict, total=False):
    """Discord server (guild)."""

    id: Required[int]  # noqa: A003
    name: Required[str]
    icon: Required[str | None]
    splash: Required[str | None]
    discovery_splash: Required[str | None]
    owner_id: Required[int]
    afk_channel_id: Required[int | None]
    afk_timeout: Required[int]
    verification_level: Required[int]
    default_message_notifications: Required[int]
    explicit_content_filter: Required[int]
    roles: Required[list[RoleData]]
    emojis: Required[list[EmojiData]]
    features: Required[list[str]]
    mfa_level: Required[int]
    application_id: Required[int | None]
    system_channel_id: Required[int | None]
    system_channel_flags: Required[int]
    rules_channel_id: Required[int | None]
    vanity_url_code: Required[str | None]
    description: Required[str | None]
    banner: Required[str | None]
    premium_tier: Required[int]
    preferred_locale: Required[str]
    public_updates_channel_id: Required[int | None]
    nsfw_level: Required[int]
    premium_progress_bar_enabled: Required[bool]

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
class VoiceStateData(TypedDict):
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

    guild_id: NotRequired[int]
    member: NotRequired[MemberData]


# https://discord.com/developers/docs/topics/gateway#presence-update-presence-update-event-fields
class PresenceUpdateData(TypedDict):
    """Presence update."""

    user: UserData
    guild_id: int
    status: str
    activities: list[ActivityData]
    client_status: ClientStatusData


# https://discord.com/developers/docs/topics/gateway#activity-object-activity-structure
class ActivityData(TypedDict, total=False):
    """Activity."""

    name: Required[str]
    type: Required[int]  # noqa: A003
    created_at: Required[int]

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

    id: str  # noqa: A003
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

    id: int  # noqa: A003
    guild_id: int
    channel_id: int
    topic: str
    privacy_level: int
    discoverable_disabled: bool


class GuildScheduledEventData(TypedDict):
    """Guild scheduled event."""

    id: int  # noqa: A003
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

    description: NotRequired[str]
    creator: NotRequired[UserData]
    user_count: NotRequired[int]


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


class ApplicationData(TypedDict):
    """Data about he bots application."""

    id: int  # noqa: A003
    owner: NotRequired[UserData]


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
class CommandStructure(TypedDict, total=False):
    """Application command structure."""

    name: Required[str]
    description: Required[str]

    type: int  # noqa: A003
    options: list[CommandOption]
    default_permission: bool


# https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-option-structure
class CommandOption(TypedDict, total=False):
    """Slash command options."""

    type: Required[int]  # noqa: A003
    name: Required[str]
    description: Required[str]

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


class InteractionEventData(TypedDict, total=False):
    """Interaction Event Data."""

    id: Required[int]  # noqa: A003
    application_id: Required[int]
    type: Required[int]  # noqa: A003
    token: Required[str]
    version: Required[Literal[1]]

    data: InteractionData
    guild_id: int
    channel_id: int
    member: MemberData
    user: UserData
    message: MessageData


class InteractionData(TypedDict, total=False):
    """Interaction Data."""

    id: Required[str]  # noqa: A003
    name: Required[str]
    type: Required[int]  # noqa: A003

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


class CommandOptionResult(TypedDict, total=False):
    """Options select in interaction."""

    name: Required[str]
    type: Required[int]  # noqa: A003

    value: str | int | float
    focused: bool


class SelectOptionValue:
    """Select option."""

    # TODO: idk anymore


class AutocompleteResponse(TypedDict):
    """Response data for a autocomplete event."""

    choices: list[CommandChoice]


class InteracionResponsData(TypedDict):
    """Response data for a interaction."""

    type: int  # noqa: A003
    data: NotRequired[AutocompleteResponse | SendMessageData]
