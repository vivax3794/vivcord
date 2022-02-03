"""Messages are the back-bone of discord."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vivcord import _typed_dicts as typed_dicts


class Message:
    """A message gotten from discord."""

    # TODO:
    pass


class SendMessageData:
    """Data that should be sent to discord when you are creating messages."""

    def __init__(self, content: str | None = None) -> None:
        """
        Create message data.

        Args:
            content (str, optional): message content. Defaults to None.
        """
        self.content = content

    def convert_to_dict(self) -> typed_dicts.SendMessageData:
        """
        Convert this object to json format.

        Returns:
            typed_dicts.SendMessageData: Created json
        """
        data: typed_dicts.SendMessageData = {}

        if self.content is not None:
            data["content"] = self.content

        return data
