from django.test import TestCase

from players.models import Player
from rounds.models import Round
from rounds.modules.first_round import RandomFirstRoundGenerator
from tournaments.models import Tournament


class FirstRoundGeneratorTests(TestCase):
    def setUp(self) -> None:
        self.tournament = Tournament.objects.create(name="test")
        self.timmy = Player.objects.create(name="timmy")
        self.edo = Player.objects.create(name="edo")
        self.tournament.players.add(self.edo, self.timmy)
        self.first_round_generator = RandomFirstRoundGenerator(
            tournament=self.tournament
        )
        self.first_round_generator.round = Round.objects.create(
            number=1, tournament=self.tournament
        )

    # TODO: mostly a duplicated test which requires a lot of setUp... probably not needed
    def test_pairings_creation(self):
        pass
