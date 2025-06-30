from typing import List

from django.shortcuts import get_object_or_404

from pairings.models import Pairing, PairingResult, PlayerEntry
from rounds.models import Round
from rounds.schemas import RoundSchema
from standings.models import Standing


def save_round_to_db(round: RoundSchema) -> None:
    current_round: Round = get_object_or_404(Round, pk=round.id)
    update_entries: List[PlayerEntry] = []
    for req_pairing in round.pairings:
        entries: List[PlayerEntry] = []
        pairing: Pairing = get_object_or_404(Pairing, pk=req_pairing.id)
        # update player entries objects
        old_entries: List[PlayerEntry] = list(pairing.entries.all())  # type: ignore
        for old_entry, new_entry in zip(old_entries, req_pairing.entries):  # type: ignore
            get_object_or_404(PlayerEntry, pk=new_entry.id)
            old_entry.wins = new_entry.wins
            entries.append(old_entry)
        # PlayerEntry.objects.bulk_update(updated_entries, ["wins"])
        update_entries += entries
        # update standings
        first_entry = entries[0]
        second_entry = entries[1]
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
    # update opponents information
    standings: List[Standing] = current_round.tournament.standings.all()
    for standing in standings:
        opponents: List[Standing] = [
            oppo.standing
            for oppo in list(standing.opponents.all())  # type: ignore
        ]
        oppo_games_won = 0
        oppo_matches_won = 0
        oppo_games_played = 0
        oppo_matches_played = 0
        for opponent in opponents:
            oppo_matches_won += opponent.matches_won
            oppo_matches_played += opponent.matches_played
            oppo_games_won += opponent.games_won
            oppo_games_played += opponent.games_played
        standing.opponents_match_winrate = oppo_matches_won / oppo_matches_played
        standing.opponents_game_winrate = oppo_games_won / oppo_games_played
    PlayerEntry.objects.bulk_update(update_entries, ["wins"])
    Standing.objects.bulk_update(
        standings, ["opponents_game_winrate", "opponents_match_winrate"]
    )
    current_round.state = Round.States.COMPLETED
    current_round.save()
