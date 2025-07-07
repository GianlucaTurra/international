from abc import ABC
from typing import List, Tuple

from django.db import transaction
from django.shortcuts import get_object_or_404

from pairings.models import Pairing, PairingResult, PlayerEntry
from pairings.schemas import PlayerEntrySchema
from rounds.models import Round
from rounds.schemas import RoundSchema
from standings.models import Standing
from tournaments.models import Tournament


class RoundSaver(ABC):
    def save(self) -> Round:  # type: ignore
        pass


class SimpleSwissRoundSaver(RoundSaver):
    def __init__(self, round: RoundSchema, current_round: Round) -> None:
        self.round = round
        self.current_round = current_round
        self.updated_entries: List[PlayerEntry] = []
        self.updated_standings: List[Standing] = []
        self.tournament: Tournament

    def save(self) -> Round:
        for req_pairing in self.round.pairings:
            pairing: Pairing = get_object_or_404(Pairing, pk=req_pairing.id)
            self.update_standings(
                *self.update_player_entries(pairing, req_pairing.entries)
            )
        self.current_round.state = Round.States.COMPLETED
        self.tournament: Tournament = self.current_round.tournament
        if self.current_round.number == self.tournament.number_of_rounds:
            self.tournament.state = Tournament.States.COMPLETED
        with transaction.atomic():
            PlayerEntry.objects.bulk_update(self.updated_entries, fields=["wins"])
            Standing.objects.bulk_update(
                self.updated_standings,
                fields=[
                    "matches_won",
                    "matches_tied",
                    "games_won",
                    "games_tied",
                    "matches_played",
                    "games_played",
                    "points",
                ],
            )
            self.update_opponents_informations()
            Standing.objects.bulk_update(
                self.updated_standings,
                fields=[
                    "opponents_match_winrate",
                    "opponents_game_winrate",
                ],
            )
            self.current_round.save()
            self.tournament.save()
        with transaction.atomic():
            if self.tournament.is_completed():
                for standing in self.tournament.standings.all():  # type: ignore
                    standing.opponents_tacker.all().delete()
        self.current_round.refresh_from_db()
        return self.current_round

    def update_player_entries(
        self, pairing: Pairing, new_entries: List[PlayerEntrySchema]
    ) -> Tuple[PlayerEntry, PlayerEntry]:
        entries: List[PlayerEntry] = []
        old_entries: List[PlayerEntry] = list(pairing.entries.all())  # type: ignore
        for old_entry, new_entry in zip(old_entries, new_entries):  # type: ignore
            get_object_or_404(PlayerEntry, pk=new_entry.id)
            old_entry.wins = new_entry.wins
            entries.append(old_entry)
        self.updated_entries += entries
        return entries[0], entries[1]

    def update_standings(
        self, first_entry: PlayerEntry, second_entry: PlayerEntry
    ) -> None:
        games_played = first_entry.wins + second_entry.wins
        if first_entry.wins > second_entry.wins:
            self.updated_standings.append(
                first_entry.update_standings(PairingResult.WIN, games_played)
            )
            self.updated_standings.append(
                second_entry.update_standings(PairingResult.LOSS, games_played)
            )
        elif second_entry.wins > first_entry.wins:
            self.updated_standings.append(
                first_entry.update_standings(PairingResult.LOSS, games_played)
            )
            self.updated_standings.append(
                second_entry.update_standings(PairingResult.WIN, games_played)
            )
        else:
            self.updated_standings.append(
                first_entry.update_standings(PairingResult.DRAW, games_played)
            )
            self.updated_standings.append(
                second_entry.update_standings(PairingResult.DRAW, games_played)
            )

    def update_opponents_informations(self) -> None:
        for standing in self.updated_standings:
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
