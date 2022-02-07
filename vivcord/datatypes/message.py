"""Messages are the back-bone of discord."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vivcord import _typed_dicts as typed_dicts
    from vivcord.datatypes import Embed


class Message:
    """A message gotten from discord."""

    # TODO:
    pass


class SendMessageData:
    """Data that should be sent to discord when you are creating messages."""

    def __init__(
        self,
        content: str | None = None,
        *,
        embed: Embed | None = None,
        embeds: list[Embed] | None = None,
    ) -> None:
        """
        Create message data.

        Args:
            content (str, optional): message content. Defaults to None.
            embed (Embed, optional): message embed. Defaults to None.
            embeds (list[Embeds], optional): list of embeds to attach. Defaults to []
        """
        self.content = content
        self.embeds = embeds or []

        if embed is not None:
            self.embeds.append(embed)

    def convert_to_dict(self) -> typed_dicts.SendMessageData:
        """
        Convert this object to json format.

        Returns:
            typed_dicts.SendMessageData: Created json
        """
        data: typed_dicts.SendMessageData = {}

        if self.content is not None:
            data["content"] = self.content

        data["embeds"] = [embed.to_json() for embed in self.embeds]

        return data
