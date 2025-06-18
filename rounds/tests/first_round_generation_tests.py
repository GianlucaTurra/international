from django.test import TestCase

from players.models import Player
from rounds.models import Round
from rounds.modules.first_round import generate_first_round
from tournaments.models import Tournament


class FirstRoundGenerationTestCase(TestCase):
    def setUp(self) -> None:
        self.tournament = Tournament.objects.create(name="Test")

    def test_empty_round(self):
        """
        If no player is passed, no rounds nor standings should be created
        """
        generate_first_round(self.tournament)
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
        generate_first_round(self.tournament)
        first_round: Round = self.tournament.rounds.get_queryset()[0]  # type: ignore
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
        generate_first_round(self.tournament)
        first_round: Round = self.tournament.rounds.get_queryset()[0]  # type: ignore
        self.assertEqual(first_round.pairings.count(), 1)  # type: ignore
