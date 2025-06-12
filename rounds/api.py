from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router

from rounds.schemas import RoundIn, RoundOut
from pairings.models import Pairing

from rounds.models import Round

router = Router()


@router.get("/{round_id}", response={200: RoundOut})
def get_round(request: HttpRequest, round_id: int):
    return get_object_or_404(Round, pk=round_id)


@router.post("/save")
def save_round(request: HttpRequest, payload: RoundIn):
    current_round: Round = get_object_or_404(Round, pk=payload.id)
    for req_pairing in payload.pairings:
        pairing: Pairing = get_object_or_404(Pairing, pk=req_pairing.id)
        for old_entry, new_entry in zip(pairing.entries.all(), req_pairing.entries):
            pass
