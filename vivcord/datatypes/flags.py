class UserFlags:
    """Discord user flags."""

    def __init__(self, flags: int) -> None:
        """
        Construct a flags instance.

        Args:
            flags (int): The user flags encoded as a int.
        """
        self._raw_flag = flags

        self.staff = bool(flags & (1 << 0))
        self.partner = bool(flags & (1 << 1))
        self.hypesquad = bool(flags & (1 << 2))
        self.bug_hunter_level_1 = bool(flags & (1 << 3))
        self.hypersquad_online_house_1 = bool(flags & (1 << 6))
        self.hypersquad_online_house_2 = bool(flags & (1 << 7))
        self.hypersquad_online_house_3 = bool(flags & (1 << 8))
        self.premium_early_supporter = bool(flags & (1 << 9))
        self.team_pseudo_user = bool(flags & (1 << 10))
        self.bug_hunter_level_2 = bool(flags & (1 << 14))
        self.partner = bool(flags & (1 << 15))
        self.verified_bot = bool(flags & (1 << 16))
        self.verified_developer = bool(flags & (1 << 17))
        self.certified_moderator = bool(flags & (1 << 18))
        self.bot_http_interactions = bool(flags & (1 << 19))

    def __str__(self) -> str:
        return str(self._raw_flag)

    def __repr__(self) -> str:
        return f"UserFlags({self._raw_flag})"

    def __int__(self) -> int:
        return self._raw_flag
