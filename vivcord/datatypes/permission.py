class Permission:
    """Discord permissions."""

    def __init__(self, permissions_int: int) -> None:
        """Parse individual permissions out of the permissions int."""
        self.create_instant_invite = (permissions_int & (2 ^ 0)) != 0
        self.kick_members = (permissions_int & (2 ^ 1)) != 0
        self.ban_members = (permissions_int & (2 ^ 2)) != 0
        self.administrator = (permissions_int & (2 ^ 3)) != 0
        self.manage_channels = (permissions_int & (2 ^ 4)) != 0
        self.manage_guild = (permissions_int & (2 ^ 5)) != 0
        self.add_reactions = (permissions_int & (2 ^ 6)) != 0
        self.view_audit_log = (permissions_int & (2 ^ 7)) != 0
        self.priority_speaker = (permissions_int & (2 ^ 8)) != 0
        self.stream = (permissions_int & (2 ^ 9)) != 0
        self.view_channel = (permissions_int & (2 ^ 10)) != 0
        self.send_messages = (permissions_int & (2 ^ 11)) != 0
        self.send_tts_messages = (permissions_int & (2 ^ 12)) != 0
        self.manage_messages = (permissions_int & (2 ^ 13)) != 0
        self.embed_links = (permissions_int & (2 ^ 14)) != 0
        self.attach_files = (permissions_int & (2 ^ 15)) != 0
        self.read_message_history = (permissions_int & (2 ^ 16)) != 0
        self.mention_everyone = (permissions_int & (2 ^ 17)) != 0
        self.use_external_emojies = (permissions_int & (2 ^ 18)) != 0
        self.view_guild_insights = (permissions_int & (2 ^ 19)) != 0
        self.connect = (permissions_int & (2 ^ 20)) != 0
        self.speak = (permissions_int & (2 ^ 21)) != 0
        self.mute_members = (permissions_int & (2 ^ 22)) != 0
        self.deafen_members = (permissions_int & (2 ^ 23)) != 0
        self.move_members = (permissions_int & (2 ^ 24)) != 0
        self.use_vad = (permissions_int & (2 ^ 25)) != 0
        self.change_nickname = (permissions_int & (2 ^ 26)) != 0
        self.manage_nicknames = (permissions_int & (2 ^ 27)) != 0
        self.manage_roles = (permissions_int & (2 ^ 28)) != 0
        self.manage_webhooks = (permissions_int & (2 ^ 29)) != 0
        self.manage_emojis_and_stickers = (permissions_int & (2 ^ 30)) != 0
        self.use_application_commands = (permissions_int & (2 ^ 31)) != 0
        self.request_to_speak = (permissions_int & (2 ^ 32)) != 0
        self.manage_events = (permissions_int & (2 ^ 33)) != 0
        self.manage_threads = (permissions_int & (2 ^ 34)) != 0
        self.create_public_threads = (permissions_int & (2 ^ 35)) != 0
        self.create_private_threads = (permissions_int & (2 ^ 36)) != 0
        self.use_external_stickers = (permissions_int & (2 ^ 37)) != 0
        self.send_messages_in_threads = (permissions_int & (2 ^ 38)) != 0
        self.start_embed_activities = (permissions_int & (2 ^ 39)) != 0
        self.moderate_members = (permissions_int & (2 ^ 40)) != 0

    def calculate_value(self) -> int:
        """Convert back to int."""
        value = 0
        value |= self.create_instant_invite << 0
        value |= self.kick_members << 1
        value |= self.ban_members << 2
        value |= self.administrator << 3
        value |= self.manage_channels << 4
        value |= self.manage_guild << 5
        value |= self.add_reactions << 6
        value |= self.view_audit_log << 7
        value |= self.priority_speaker << 8
        value |= self.stream << 9
        value |= self.view_channel << 10
        value |= self.send_messages << 11
        value |= self.send_tts_messages << 12
        value |= self.manage_messages << 13
        value |= self.embed_links << 14
        value |= self.attach_files << 15
        value |= self.read_message_history << 16
        value |= self.mention_everyone << 17
        value |= self.use_external_emojies << 18
        value |= self.view_guild_insights << 19
        value |= self.connect << 20
        value |= self.speak << 21
        value |= self.mute_members << 22
        value |= self.deafen_members << 23
        value |= self.move_members << 24
        value |= self.use_vad << 25
        value |= self.change_nickname << 26
        value |= self.manage_nicknames << 27
        value |= self.manage_roles << 28
        value |= self.manage_webhooks << 29
        value |= self.manage_emojis_and_stickers << 30
        value |= self.use_application_commands << 31
        value |= self.request_to_speak << 32
        value |= self.manage_events << 33
        value |= self.manage_threads << 34
        value |= self.create_public_threads << 35
        value |= self.create_private_threads << 36
        value |= self.use_external_stickers << 37
        value |= self.send_messages_in_threads << 38
        value |= self.start_embed_activities << 39
        value |= self.moderate_members << 40
        return value
