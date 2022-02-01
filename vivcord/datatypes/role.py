from __future__ import annotations

from typing import TYPE_CHECKING

from vivcord.datatypes.permission import Permission
from vivcord.datatypes.snowflake import Snowflake

if TYPE_CHECKING:
    from vivcord import _typed_dicts as type_dicts
    from vivcord.client import Client


class Role:
    """Discord role."""

    def __init__(self, client: Client, data: type_dicts.RoleData):
        """
        Create role.

        Args:
            client (Client): vivcord client
            data (type_dicts.RoleData): role json data
        """
        self._client = client
        self._raw_data = data

        self.id = Snowflake(data["id"])
        self.name = data["name"]
        self.color = data["color"]
        self.hoisted = data["hoist"]
        self.position = data["position"]
        self.permissions = Permission(int(data["permissions"]))
        self.managed = data["managed"]
        self.mentionable = data["mentionable"]
