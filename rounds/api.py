from typing import List

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router

from international.schemas import ErrorMessage
from rounds.models import Round
from rounds.modules.generate_round import generate_round
from rounds.modules.save_round import save_round_to_db
from rounds.schemas import RoundSchema
from standings.schemas import StandingOut
from tournaments.models import Tournament
from tournaments.schemas import TournamentSelector

router = Router()

# TODO: With pydantic validators no 404 should raise anymore


@router.put("/save", response={200: List[StandingOut], 400: ErrorMessage})
def save_round(request: HttpRequest, payload: RoundSchema):
    """
    Save round's results to database updating standings and opponents'
    informations for each player.
    Only available for not completed rounds.
    """
    current_round = Round.objects.get(pk=payload.id)
    if current_round.state is Round.States.COMPLETED:
        return 400, ErrorMessage(content=f"Round {current_round.pk} already completed")
    save_round_to_db(payload)
    current_round.refresh_from_db()
    return current_round.tournament.standings.all()


@router.post("/next", response={201: RoundSchema, 400: ErrorMessage})
def create_next_round(request: HttpRequest, payload: TournamentSelector):
    """
    Not available if the tournament's last round is not completed.
    """
    tournament = Tournament.objects.get(pk=payload.id)
    if tournament.rounds.latest().state is not Round.States.COMPLETED:  # type: ignore
        return 400, ErrorMessage(
            content=f"Tournament {tournament.name} lates round is not completed"
        )
    return 201, generate_round(tournament)


@router.get("/{round_id}", response={200: RoundSchema, 404: None})
def get_round(request: HttpRequest, round_id: int):
    return get_object_or_404(Round, pk=round_id)
