from typing import Optional

from ninja import Schema


class PlayerIn(Schema):
    id: Optional[int] = None
    name: str


class PlayerOut(Schema):
    id: int
    name: str
