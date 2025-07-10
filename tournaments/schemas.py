from typing import Annotated

from ninja import Schema
from pydantic import AfterValidator, ValidationError

from players.schemas import PlayerIn, PlayerOut
from rounds.schemas import RoundSchema
from standings.schemas import StandingOut
from tournaments.models import Tournament


def exists(id) -> int:
    try:
        return Tournament.objects.get(pk=id).pk
    except Tournament.DoesNotExist as e:
        raise ValidationError(f"Tournament id {id} does not exists") from e


class TournamnetIn(Schema):
    name: str
    players: list[PlayerIn] | None = None


class TournamentOut(Schema):
    id: int
    name: str
    players: list[PlayerOut] | None = None
    rounds: list[RoundSchema] | None = None
    standings: list[StandingOut] | None = None


class TournamentSelector(Schema):
    id: Annotated[int, AfterValidator(exists)]
