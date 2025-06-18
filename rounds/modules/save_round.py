from typing import List

from django.shortcuts import get_object_or_404

from pairings.models import Pairing, PairingResult, PlayerEntry
from pairings.schemas import PairingSchema

updated_entries: List[PlayerEntry] = []


# TODO: this raises 404 exceptions, test if they are properly handled by django
def save_round_to_db(pairings: List[PairingSchema]):
    for req_pairing in pairings:
        pairing: Pairing = get_object_or_404(Pairing, pk=req_pairing.id)
        update_player_entries(pairing, req_pairing)
    update_standings()


def update_player_entries(pairing: Pairing, req_pairing: PairingSchema):
    old_entries: List[PlayerEntry] = list(pairing.entries.all())  # type: ignore
    for old_entry, new_entry in zip(old_entries, req_pairing.entries):  # type: ignore
        get_object_or_404(PlayerEntry, pk=new_entry.id)
        old_entry.wins = new_entry.wins
        updated_entries.append(old_entry)
    PlayerEntry.objects.bulk_update(updated_entries, ["wins"])


def update_standings():
    # TODO: should know better if it's 1v1
    first_entry = updated_entries[0]
    second_entry = updated_entries[1]
    games_played = first_entry.wins + second_entry.wins
    if first_entry.wins > second_entry.wins:
        first_entry.update_standings(PairingResult.WIN, games_played)
        second_entry.update_standings(PairingResult.LOSS, games_played)
    elif second_entry.wins > first_entry.wins:
        first_entry.update_standings(PairingResult.LOSS, games_played)
        second_entry.update_standings(PairingResult.WIN, games_played)
    else:
        first_entry.update_standings(PairingResult.DRAW, games_played)
        second_entry.update_standings(PairingResult.DRAW, games_played)
