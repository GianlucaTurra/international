from typing import Annotated, List, Optional

from ninja import Schema
from pydantic import AfterValidator, ValidationError

from players.schemas import PlayerIn, PlayerOut
from rounds.schemas import RoundSchema
from standings.schemas import StandingOut
from tournaments.models import Tournament


def exists(id) -> int:
    try:
        return Tournament.objects.get(pk=id).pk
    except Tournament.DoesNotExist:
        raise ValidationError(f"Tournament id {id} does not exists")


class TournamnetIn(Schema):
    name: str
    players: Optional[List[PlayerIn]] = None


class TournamentOut(Schema):
    id: int
    name: str
    players: Optional[List[PlayerOut]] = None
    rounds: Optional[List[RoundSchema]] = None
    standings: Optional[List[StandingOut]] = None


class TournamentSelector(Schema):
    id: Annotated[int, AfterValidator(exists)]
