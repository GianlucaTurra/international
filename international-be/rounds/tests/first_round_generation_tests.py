from django.test import TestCase

from players.models import Player
from rounds.modules.round_manager_factory import get_first_round_generator
from tournaments.models import Tournament


class FirstRoundGenerationTestCase(TestCase):
    def setUp(self) -> None:
        self.tournament = Tournament.objects.create(name="Test")

    def test_empty_round(self):
        """
        If no player is passed, no rounds nor standings should be created
        """
        get_first_round_generator(self.tournament).generate_round()
        self.tournament.refresh_from_db()
        self.assertEqual(self.tournament.rounds.count(), 0)  # type: ignore
        self.assertEqual(self.tournament.standings.count(), 0)  # type: ignore

    def test_even_number_of_players(self):
        self.tournament.players.add(
            *[
                Player.objects.create(name="Roborbio"),
                Player.objects.create(name="Stefano"),
            ]
        )
        first_round = get_first_round_generator(self.tournament).generate_round()
        self.assertEqual(first_round.pairings.count(), 1)  # type: ignore

    def test_odd_number_of_players(self):
        """
        This should NOT create 2 pairings, the creation of the fake player is delegated
        to the tournament itself in the start function.
        """
        self.tournament.players.add(
            *[
                Player.objects.create(name="Roborbio"),
                Player.objects.create(name="Stefano"),
                Player.objects.create(name="Eliminiano"),
            ]
        )
        first_round = get_first_round_generator(self.tournament).generate_round()
        self.assertEqual(first_round.pairings.count(), 1)  # type: ignore
