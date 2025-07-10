from abc import ABC, abstractmethod

from django.db import transaction

from pairings.models import Pairing, PlayerEntry
from rounds.models import Round
from standings.models import Standing
from tournaments.models import Tournament


class RoundGenerator(ABC):
    @abstractmethod
    def generate_round(self) -> Round:
        pass


class SimpleSwissRoundGenerator(RoundGenerator):
    def __init__(self, tournament: Tournament) -> None:
        self.tournament = tournament
        self.new_round = Round(
            number=self.tournament.rounds.count() + 1,  # type: ignore
            tournament=self.tournament,
            state=Round.States.ONGOING,
        )
        self.standings: list[Standing] = list(self.tournament.standings.all())  # type: ignore
        self.pairings: list[Pairing] = []
        self.player_entries: list[PlayerEntry] = []

    def generate_round(self) -> Round:
        while len(self.standings) > 0:
            standing = self.standings[0]
            new_opponent: Standing
            opponents_already_faced: set[Standing] = set(standing.opponents.all())  # type: ignore
            for s in self.standings[1:]:
                if s in opponents_already_faced:
                    continue
                new_opponent = s
                break
            pairing = Pairing(round=self.new_round)
            entry_1 = PlayerEntry(
                pairing=pairing, player=standing.player, standing=standing
            )
            entry_2 = PlayerEntry(
                pairing=pairing,
                player=new_opponent.player,  # type: ignore
                standing=new_opponent,  # type: ignore
            )
            self.pairings.append(pairing)
            self.player_entries.append(entry_1)
            self.player_entries.append(entry_2)
            self.standings.pop(0)
            self.standings.pop(self.standings.index(new_opponent))  # type: ignore
        with transaction.atomic():
            self.new_round.save()
            Standing.objects.bulk_create(self.standings)
            Pairing.objects.bulk_create(self.pairings)
            PlayerEntry.objects.bulk_create(self.player_entries)
        return self.new_round
