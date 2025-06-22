import random
from typing import Dict, List

from pairings.models import Pairing, PlayerEntry
from players.models import Player
from rounds.models import Round
from standings.models import OpponentsTracker, Standing
from tournaments.models import Tournament


class FirstRoundGenerator:
    def __init__(self, tournament: Tournament) -> None:
        self.standings: List[Standing] = []
        self.tournament: Tournament = tournament
        self.round: Round
        self.players: List[Player] = list(self.tournament.players.all())
        self.players_mid_number: int = len(self.players) // 2
        self.pairings: List[Pairing] = []
        self.player_entries: List[PlayerEntry] = []
        self.standings_cache: Dict[str, Standing] = {}
        self.opponents_trackers: List[OpponentsTracker] = []

    def generate(self):
        if self.players == []:
            return
        self.round = Round.objects.create(number=1, tournament=self.tournament)
        random.shuffle(self.players)
        self.create_standings()
        self.create_pairings()
        Standing.objects.bulk_create(self.standings)
        Pairing.objects.bulk_create(self.pairings)
        PlayerEntry.objects.bulk_create(self.player_entries)
        OpponentsTracker.objects.bulk_create(self.opponents_trackers)

    def create_standings(self):
        for player in self.players:
            standing = Standing(player=player, tournament=self.tournament)
            self.standings.append(standing)
            self.standings_cache[player.name] = standing

    def create_pairings(self):
        first_half, second_half = (
            self.players[: self.players_mid_number],
            self.players[self.players_mid_number :],
        )
        for p1, p2 in zip(first_half, second_half):
            pairing = Pairing(round=self.round)
            self.pairings.append(pairing)
            self.player_entries.append(
                PlayerEntry(
                    pairing=pairing, player=p1, standing=self.standings_cache[p1.name]
                )
            )
            self.player_entries.append(
                PlayerEntry(
                    pairing=pairing, player=p2, standing=self.standings_cache[p2.name]
                )
            )
            self.opponents_trackers.append(
                OpponentsTracker(
                    standing=self.standings_cache[p1.name],
                    opponent=self.standings_cache[p2.name],
                    round=self.round,
                )
            )
            self.opponents_trackers.append(
                OpponentsTracker(
                    standing=self.standings_cache[p2.name],
                    opponent=self.standings_cache[p1.name],
                    round=self.round,
                )
            )
