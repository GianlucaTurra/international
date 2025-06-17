from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router

from rounds.models import Round
from rounds.modules.save_round import save_round_to_db
from rounds.schemas import RoundIn, RoundOut
from standings.schemas import StandingOut

router = Router()


@router.put("/save", response={200: StandingOut})
def save_round(request: HttpRequest, payload: RoundIn):
    current_round = get_object_or_404(Round, pk=payload.id)
    save_round_to_db(payload.pairings)
    current_round.refresh_from_db()
    return current_round.tournament.standings


@router.get("/{round_id}", response={200: RoundOut})
def get_round(request: HttpRequest, round_id: int):
    return get_object_or_404(Round, pk=round_id)
