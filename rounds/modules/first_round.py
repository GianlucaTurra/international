import random
from abc import ABC, abstractmethod

from django.db import transaction

from pairings.models import Pairing, PlayerEntry
from players.models import Player
from rounds.models import Round
from standings.models import OpponentsTracker, Standing
from tournaments.models import Tournament


class FirstRoundGenerator(ABC):
    @abstractmethod
    def generate_round(self) -> Round | None:
        pass


class RandomFirstRoundGenerator(FirstRoundGenerator):
    """
    Class to generate the first round of a Swiss tournament. The rule for the
    first round is to create random pairings with no seeds.
    """

    def __init__(self, tournament: Tournament) -> None:
        self.standings: list[Standing] = []
        self.tournament: Tournament = tournament
        self.round: Round
        self.players: list[Player] = list(self.tournament.players.all())
        self.players_mid_number: int = len(self.players) // 2
        self.pairings: list[Pairing] = []
        self.player_entries: list[PlayerEntry] = []
        self.standings_cache: dict[str, Standing] = {}
        self.opponents_trackers: list[OpponentsTracker] = []

    def generate_round(self) -> Round | None:
        if self.players == []:
            return
        self.round = Round.objects.create(number=1, tournament=self.tournament)
        random.shuffle(self.players)
        self.create_standings()
        self.create_pairings()
        with transaction.atomic():
            Standing.objects.bulk_create(self.standings)
            Pairing.objects.bulk_create(self.pairings)
            PlayerEntry.objects.bulk_create(self.player_entries)
            OpponentsTracker.objects.bulk_create(self.opponents_trackers)
        return self.round

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
        for p1, p2 in zip(first_half, second_half, strict=True):
            pairing = Pairing(round=self.round)
            self.pairings.append(pairing)
            self.player_entries.append(
                PlayerEntry(
                    pairing=pairing,
                    player=p1,
                    standing=self.standings_cache[p1.name],
                )
            )
            self.player_entries.append(
                PlayerEntry(
                    pairing=pairing,
                    player=p2,
                    standing=self.standings_cache[p2.name],
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
