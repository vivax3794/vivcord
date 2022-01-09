"""Communicate with the discord api."""

from __future__ import annotations

from typing import TYPE_CHECKING

import aiohttp
from loguru import logger

from . import errors
from ._constants import BASE_URL

if TYPE_CHECKING:
    from . import _internal_types as internal
    from . import datatypes


class Api:
    """Communicate with the discord api."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """
        Create a api instance.

        Args:
            session (aiohttp.ClientSession): The http session to use.
        """
        self.session = session
        self.application_id: datatypes.Snowflake | None = None

    async def _handle_response(self, response: aiohttp.ClientResponse) -> None:
        logger.debug(response.status)

        if response.status >= 400:
            raw_error = await response.json()
            raise errors.create_http_error(response.status, raw_error)

    async def get_gateway(self) -> str:
        """
        Get gateway url.

        Returns:
            str: the gateway url.
        """
        # https://discord.com/developers/docs/topics/gateway#get-gateway
        async with self.session.get(f"{BASE_URL}/gateway") as resp:
            await self._handle_response(resp)
            data = await resp.json()
            return data["url"]

    async def register_command(self, command: internal.CommandStructure) -> None:
        """
        Register a application command.

        Args:
            command (internal.CommandStructure): Data for command
        """
        # https://discord.com/developers/docs/interactions/application-commands#create-global-application-command
        logger.info(f"registering global command {command['name']!r}")

        async with self.session.post(
            f"{BASE_URL}/applications/{self.application_id}/commands", json=command
        ) as resp:
            await self._handle_response(resp)

    async def register_guild_command(
        self, guild_id: datatypes.Snowflake | int, command: internal.CommandStructure
    ) -> None:
        """
        Regiser a application command for only 1 guild.

        Args:
            guild_id (datatypes.Snowflake): Guild to register in.
            command (internal.CommandStructure): Data for command
        """
        # https://discord.com/developers/docs/interactions/application-commands#create-guild-application-command
        logger.info(
            f"registering guild command {command['name']!r} on guild {guild_id!r}"
        )

        logger.debug(self.session.headers)

        async with self.session.post(
            f"{BASE_URL}/applications/{self.application_id}/guilds/{guild_id}/commands",
            json=command,
        ) as resp:
            await self._handle_response(resp)

    async def overwrite_global_commands(
        self, commands: list[internal.CommandStructure]
    ) -> None:
        """
        Overwrite all global commands.

        Args:
            commands (list[internal.CommandStructure]): List of commands.
        """
        # https://discord.com/developers/docs/interactions/application-commands#bulk-overwrite-global-application-commands
        logger.info("overwriting global commands")

        async with self.session.put(
            f"{BASE_URL}/applications/{self.application_id}/commands", json=commands
        ) as resp:
            await self._handle_response(resp)

    async def overwrite_guild_commands(
        self,
        guild_id: datatypes.Snowflake | int,
        commands: list[internal.CommandStructure],
    ) -> None:
        """
        Overwrite all guild commands.

        Args:
            guild_id (datatypes.Snowflake): Guild to overwrite in.
            commands (list[internal.CommandStructure]): List of commands.
        """
        # https://discord.com/developers/docs/interactions/application-commands#bulk-overwrite-guild-application-commands
        logger.info(f"overwriting guild commands on guild {guild_id!r}")

        async with self.session.put(
            f"{BASE_URL}/applications/{self.application_id}/guilds/{guild_id}/commands",
            json=commands,
        ) as resp:
            await self._handle_response(resp)

    async def respond_to_interaction(
        self, int_id: int, int_token: str, data: dict[str, object]
    ) -> None:
        logger.debug(f"responding to interaction {int_id}")

        async with self.session.post(
            f"{BASE_URL}/interactions/{int_id}/{int_token}/callback", json=data
        ) as resp:
            await self._handle_response(resp)
