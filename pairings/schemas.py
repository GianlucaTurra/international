from typing import List
from ninja import Schema

from players.schemas import PlayerOut


class PlayerEntrySchema(Schema):
    id: int | None = None
    player: PlayerOut
    wins: int


class PairingSchema(Schema):
    id: int
    entries: List[PlayerEntrySchema]
