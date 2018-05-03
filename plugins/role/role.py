from typing import List


class Role(object):
    role_name: str = None
    aliases: List[str] = []
    restricted: bool = False
    parent: str = None

    def __init__(
            self, role_name=None, aliases=list(), restricted=False,
            parent=None
    ):
        self.role_name = role_name
        self.aliases = aliases
        self.restricted = restricted
        self.parent = parent
