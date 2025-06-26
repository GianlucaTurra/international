from ninja import Schema


class PlayerIn(Schema):
    id: int | None = None
    name: str


class PlayerOut(Schema):
    id: int
    name: str
    is_placeholder: bool
