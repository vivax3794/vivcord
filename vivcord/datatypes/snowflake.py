"""Snowflakes are like fancy ids that contain info."""

from __future__ import annotations

from datetime import datetime

# https://discord.com/developers/docs/reference#convert-snowflake-to-datetime
DISCORD_EPOCH = 1420070400000


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
        self.type_dicts_worker_id = (snowflake_id & 0x3E0000) >> 17
        self.type_dicts_process_id = (snowflake_id & 0x1F000) >> 12
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
