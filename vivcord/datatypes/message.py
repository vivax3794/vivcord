from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vivcord import _typed_dicts as typed_dicts

class Message:
    # TODO:
    pass


class SendMessageData:
    def __init__(self, content: str | None) -> None:
        self.content = content

    def convert_to_dict(self) -> typed_dicts.SendMessageData:
        data: typed_dicts.SendMessageData = {}

        if self.content is not None:
            data["content"] = self.content

        return data