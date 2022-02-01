from __future__ import annotations

from datetime import datetime
from enum import IntEnum
from typing import TYPE_CHECKING

from vivcord.datatypes.flags import UserFlags
from vivcord.datatypes.permission import Permission
from vivcord.datatypes.snowflake import Snowflake

if TYPE_CHECKING:
    from vivcord import Client
    from vivcord import _typed_dicts as type_dicts


# https://discord.com/developers/docs/resources/user#user-object-premium-types
class NitroType(IntEnum):
    """The users nitro type."""

    Nothing = 0
    Classic = 1
    Nitro = 2


# https://discord.com/developers/docs/resources/user#user-object-user-structure
class User:
    """Reperesents a user."""

    def __init__(self, client: Client, data: type_dicts.UserData) -> None:
        """
        Construct a User instance.

        You should not construct this yourself.

        Args:
            client (Client): Discord client
            data (type_dicts.UserData): The raw user data
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


# https://discord.com/developers/docs/resources/guild#guild-member-object
class Member:
    """Discord member."""

    def __init__(self, client: Client, data: type_dicts.MemberData) -> None:
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
