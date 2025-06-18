from typing import List

from django.shortcuts import get_object_or_404

from pairings.models import Pairing, PairingResult, PlayerEntry
from rounds.schemas import RoundIn


def save_round_to_db(round: RoundIn):
    for req_pairing in round.pairings:
        updated_entries: List[PlayerEntry] = []
        pairing: Pairing = get_object_or_404(Pairing, pk=req_pairing.id)
        old_entries: List[PlayerEntry] = list(pairing.entries.all())  # type: ignore
        for old_entry, new_entry in zip(old_entries, req_pairing.entries):  # type: ignore
            get_object_or_404(PlayerEntry, pk=new_entry.id)
            old_entry.wins = new_entry.wins
            updated_entries.append(old_entry)
        PlayerEntry.objects.bulk_update(updated_entries, ["wins"])
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
