"""Embeds allows you to create nicer messages."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vivcord import _typed_dicts as type_dicts


class Embed:
    """Discord embed."""

    def __init__(
        self,
        title: str | None = None,
        description: str | None = None,
        url: str | None = None,
        timestamp: datetime | None = None,
        color: int | None = None,
        footer: EmbedFooter | None = None,
        image: EmbedImage | None = None,
        thumbnail: EmbedThumbnail | None = None,
    ) -> None:
        """
        Create embed.

        Args:
            title (str, optional): embed title. Defaults to None.
            description (str, optional): embed description. Defaults to None.
            url (str, optional): embed linked url. Defaults to None.
            timestamp (datetime, optional): embed timestamp. Defaults to None.
            color (int, optional): embed color. Defaults to None.
            footer (EmbedFooter, optional): embed. Defaults to None.
            image (EmbedImage, optional): embed image. Defaults to None.
            thumbnail (EmbedThumbnail, optional): embed thumbnail. Defaults to None.
        """
        self.title = title
        self.description = description
        self.url = url
        self.timestamp = timestamp
        self.color = color
        self.footer = footer
        self.image = image
        self.thumbnail = thumbnail

    def set_footer(self, text: str, icon_url: str | None = None) -> None:
        """
        Set embed footer.

        Args:
            text (str): Text for footer
            icon_url (str, optional): Icon to show in footer. Defaults to None.
        """
        self.footer = EmbedFooter(text, icon_url)

    @classmethod
    def from_json(cls, data: type_dicts.EmbedData) -> Embed:
        """
        Create Embed from json data.

        Args:
            data (type_dicts.EmbedFooterData): json data

        Returns:
            Embed: Created embed
        """
        return cls(
            data.get("title"),
            data.get("description"),
            data.get("url"),
            datetime.fromtimestamp(int(data["timestamp"]))
            if "timestamp" in data
            else None,
            data.get("color"),
            EmbedFooter.from_json(data["footer"]) if "footer" in data else None,
            EmbedImage.from_json(data["image"]) if "image" in data else None,
        )

    def to_json(self) -> type_dicts.EmbedData:
        """
        Convert to json.

        Returns:
            type_dicts.EmbedData: Json data
        """
        data: type_dicts.EmbedData = {}

        if self.title:
            data["title"] = self.title
        if self.description:
            data["description"] = self.description
        if self.url:
            data["url"] = self.url
        if self.timestamp:
            data["timestamp"] = str(int(self.timestamp.timestamp()))
        if self.color:
            data["color"] = self.color
        if self.footer:
            data["footer"] = self.footer.to_json()
        if self.image:
            data["image"] = self.image.to_json()

        return data


class EmbedFooter:
    """Embed footer."""

    def __init__(
        self,
        text: str,
        icon_url: str | None = None,
    ) -> None:
        """
        Create embed footer.

        Args:
            text (str): Footer text
            icon_url (str, optional): Footer icon. Defaults to None.
        """
        self.text = text
        self.icon_url = icon_url

    @classmethod
    def from_json(cls, data: type_dicts.EmbedFooterData) -> EmbedFooter:
        """
        Create footer from json.

        Args:
            data (type_dicts.EmbedFooterData): json data

        Returns:
            EmbedFooter: Created footer
        """
        return cls(
            data["text"],
            data.get("icon_url"),
        )

    def to_json(self) -> type_dicts.EmbedFooterData:
        """
        Convert to json.

        Returns:
            type_dicts.EmbedFooterData: Created json
        """
        data: type_dicts.EmbedFooterData = {"text": self.text}
        if self.icon_url:
            data["icon_url"] = self.icon_url

        return data


class EmbedImage:
    """Embed image."""

    def __init__(
        self, url: str, height: int | None = None, width: int | None = None
    ) -> None:
        """
        Create embed image.

        Args:
            url (str): img url
            height (int): img height
            width (int): img width
        """
        self.url = url
        self.width = width
        self.height = height

    @classmethod
    def from_json(cls, data: type_dicts.EmbedImageData) -> EmbedImage:
        """
        Create EmbedImage from json data.

        Args:
            data (type_dicts.EmbedImageData): Json data

        Returns:
            EmbedImage: Image created from json
        """
        return cls(data["url"], data.get("width"), data.get("height"))

    def to_json(self) -> type_dicts.EmbedImageData:
        """
        Convert img to json.

        Returns:
            type_dicts.EmbedImageData: Created json
        """
        data: type_dicts.EmbedImageData = {"url": self.url}

        if self.height is not None:
            data["height"] = self.height
        if self.width is not None:
            data["width"] = self.width

        return data


class EmbedThumbnail:
    """Embed thumbnail."""

    def __init__(
        self, url: str, height: int | None = None, width: int | None = None
    ) -> None:
        """
        Create embed thumbnail.

        Args:
            url (str): img url
            height (int): img height
            width (int): img width
        """
        self.url = url
        self.width = width
        self.height = height

    @classmethod
    def from_json(cls, data: type_dicts.EmbedThumbnailData) -> EmbedThumbnail:
        """
        Create EmbedThumbnail from json data.

        Args:
            data (type_dicts.EmbedThumbnailData): Json data

        Returns:
            EmbedThumbnail: Thumbnail created from json
        """
        return cls(data["url"], data.get("width"), data.get("height"))

    def to_json(self) -> type_dicts.EmbedThumbnailData:
        """
        Convert thumbnail to json.

        Returns:
            type_dicts.EmbedThumbnailData: Created json
        """
        data: type_dicts.EmbedThumbnailData = {"url": self.url}

        if self.height is not None:
            data["height"] = self.height
        if self.width is not None:
            data["width"] = self.width

        return data
