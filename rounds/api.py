from typing import List

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router

from rounds.models import Round
from rounds.modules.generate_round import generate_round
from rounds.modules.save_round import save_round_to_db
from rounds.schemas import RoundSchema
from standings.schemas import StandingOut
from tournaments.models import Tournament
from tournaments.schemas import TournamentSelector

router = Router()


@router.put("/save", response={200: List[StandingOut], 404: None})
def save_round(request: HttpRequest, payload: RoundSchema):
    """
    Save round's results to database updating standings and opponents'
    informations for each player.
    If no round is found for the given id 404 response is given.
    """
    current_round = get_object_or_404(Round, pk=payload.id)
    save_round_to_db(payload)
    current_round.refresh_from_db()
    return current_round.tournament.standings.all()


@router.post("/next", response={201: RoundSchema, 404: None})
def create_next_round(request: HttpRequest, payload: TournamentSelector):
    """
    If no tournament is found for the given id a 404 response is given.
    """
    tournament = get_object_or_404(Tournament, pk=payload.id)
    return 201, generate_round(tournament)


@router.get("/{round_id}", response={200: RoundSchema, 404: None})
def get_round(request: HttpRequest, round_id: int):
    return get_object_or_404(Round, pk=round_id)
