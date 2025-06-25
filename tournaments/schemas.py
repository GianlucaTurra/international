from typing import List
from ninja import Schema
from rounds.schemas import RoundOut
from players.schemas import PlayerIn, PlayerOut
from standings.schemas import StandingOut


class TournamnetIn(Schema):
    name: str
    players: List[PlayerIn] | None = None


class TournamentOut(Schema):
    id: int
    name: str
    players: List[PlayerOut] | None = None
    rounds: List[RoundOut] | None = None
    standings: List[StandingOut] | None = None


class TournamentSelector(Schema):
    id: int
