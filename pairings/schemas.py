from typing import List, Optional

from ninja import Schema

from players.schemas import PlayerOut


class PlayerEntrySchema(Schema):
    id: Optional[int] = None
    player: PlayerOut
    wins: int
    draws: int


class PairingSchema(Schema):
    id: int
    entries: List[PlayerEntrySchema]
