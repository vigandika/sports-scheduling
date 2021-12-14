from typing import Optional


class Team:

    def __init__(self, id: int, name: str, category: Optional[str]):
        self.id = id
        self.name = name
        self.category = category
        self.assigned_index = None
