"""Communicate with the discord api."""

import aiohttp
from loguru import logger

from . import errors
from ._constants import BASE_URL


class Api:
    """Communicate with the discord api."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """
        Create a api instance.

        Args:
            session (aiohttp.ClientSession): The http session to use.
        """
        self.session = session

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
