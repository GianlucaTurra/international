from typing import List
from ninja import Schema

from pairings.schemas import PairingSchema


class RoundIn(Schema):
    id: int
    pairings: List[PairingSchema]


class RoundOut(Schema):
    id: int
    number: int
    pairings: List[PairingSchema]
