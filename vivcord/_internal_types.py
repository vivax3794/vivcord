from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

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


# https://discord.com/developers/docs/topics/gateway#payloads-gateway-payload-structure
class GatewayResponse(TypedDict):
    """Gateway response."""

    op: int
    d: dict[str, Any]
    s: int | None
    t: str | None


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


# https://discord.com/developers/docs/resources/application#application-object
# TODO: most of this
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
