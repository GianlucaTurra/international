from typing import List

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router

from pairings.models import Pairing, PlayerEntry
from rounds.models import Round
from rounds.schemas import RoundIn, RoundOut
from standings.models import Standing

router = Router()


@router.put("/save", response={200: RoundOut})
def save_round(request: HttpRequest, payload: RoundIn):
    current_round = get_object_or_404(Round, pk=payload.id)
    for req_pairing in payload.pairings:
        pairing: Pairing = get_object_or_404(Pairing, pk=req_pairing.id)

        # Update entries with given results
        updated_entries: List[PlayerEntry] = []
        old_entries: List[PlayerEntry] = list(pairing.entries.all())  # type: ignore
        for old_entry, new_entry in zip(old_entries, req_pairing.entries):  # type: ignore
            get_object_or_404(PlayerEntry, pk=new_entry.id)
            old_entry.wins = new_entry.wins
            updated_entries.append(old_entry)
        updated_rows: int = PlayerEntry.objects.bulk_update(updated_entries, ["wins"])
        assert updated_rows == len(updated_entries)  # TODO: handle this case

        # Based on update entries update the standings
        # TODO: for now let's assume all matches are 1v1
        first_entry = updated_entries[0]
        second_entry = updated_entries[1]
        first_player_standing = Standing.objects.get(player=first_entry.player)
        second_player_standing = Standing.objects.get(player=second_entry.player)
        first_player_standing.games_won += first_entry.wins
        second_player_standing.games_won += second_entry.wins
        if first_entry.wins > second_entry.wins:
            first_player_standing.matches_won += 1
        if second_entry.wins > first_entry.wins:
            second_player_standing.matches_won += 1
        Standing.objects.bulk_update(
            [first_player_standing, second_player_standing],
            ["games_won", "matches_won"],
        )
    current_round.refresh_from_db()
    return current_round


@router.get("/{round_id}", response={200: RoundOut})
def get_round(request: HttpRequest, round_id: int):
    return get_object_or_404(Round, pk=round_id)
