from dataclasses import dataclass


@dataclass
class Intents:
    """Intents describes what values should be passed from discord."""

    guilds: bool = False
    guild_members: bool = False
    guild_bans: bool = False
    guild_emojis_and_stickers: bool = False
    guild_integrations: bool = False
    guild_webhooks: bool = False
    guild_invites: bool = False
    guild_voice_states: bool = False
    guild_presences: bool = False
    guild_messages: bool = False
    guild_message_reactions: bool = False
    guild_message_typing: bool = False
    direct_message: bool = False
    direct_message_reactions: bool = False
    direct_message_typing: bool = False
    guild_scheduled_events: bool = False

    def calculate_value(self) -> int:
        """
        Convert intents to int so it can be sent to discord.

        Returns:
            int: Resulting int
        """
        value = 0
        value |= self.guilds << 0
        value |= self.guild_members << 1
        value |= self.guild_bans << 2
        value |= self.guild_emojis_and_stickers << 3
        value |= self.guild_integrations << 4
        value |= self.guild_webhooks << 5
        value |= self.guild_invites << 6
        value |= self.guild_voice_states << 7
        value |= self.guild_presences << 8
        value |= self.guild_messages << 9
        value |= self.guild_message_reactions << 10
        value |= self.guild_message_typing << 11
        value |= self.direct_message << 12
        value |= self.guild_scheduled_events << 16
        return value
