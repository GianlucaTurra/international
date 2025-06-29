import json

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse_lazy

from rounds.models import Round
from standings.models import OpponentsTracker
from tournaments.models import Tournament

TOURNAMENT_WITH_EMPTY_PLAYERS = {"name": "test", "players": []}
TOURNAMENT_WITH_EVEN_NUMBER_OF_PLAYERS = {
    "name": "test",
    "players": [
        {"name": "Pito"},
        {"name": "Gianni del Baretto"},
        {"name": "Sgnagnez"},
        {"name": "Gigi Pistoia"},
    ],
}
TOURNAMENT_WITH_ODD_NUMBER_OF_PLAYERS = {
    "name": "test",
    "players": [
        {"name": "Pito"},
        {"name": "Gianni del Baretto"},
        {"name": "Gino"},
        {"name": "Sgnagnez"},
        {"name": "Gigi Pistoia"},
    ],
}


class CreateTournamentTestCase(TestCase):
    """
    Class to test the create tournament endpoint
    """

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="gino", password="gino", email="ginoilpostino@email.com"
        )
        self.client = Client()
        auth_resp = self.client.post(
            reverse_lazy("api-1.0.0:token_obtain_pair"),
            {"username": "gino", "password": "gino"},
            content_type="application/json",
        )
        assert auth_resp.status_code == 200
        self.token = auth_resp.json()["access"]
        self.url = reverse_lazy("api-1.0.0:create_tournament")

    def test_no_body_request(self):
        response = self.client.post(self.url, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertGreaterEqual(response.status_code, 400)

    def test_tournament_creation_with_empty_players(self):
        """
        If no player is passed the tournament should be created without
        players, rounds or standings
        """
        response = self.client.post(
            self.url,
            json.dumps(TOURNAMENT_WITH_EMPTY_PLAYERS),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tournament.objects.count(), 1)
        tournament = Tournament.objects.get(pk=1)
        self.assertEqual(tournament.players.count(), 0)
        self.assertEqual(tournament.rounds.count(), 0)  # type: ignore
        self.assertEqual(tournament.standings.count(), 0)  # type: ignore

    def test_tournament_creation_with_new_player(self):
        response = self.client.post(
            self.url,
            json.dumps(TOURNAMENT_WITH_EVEN_NUMBER_OF_PLAYERS),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tournament.objects.count(), 1)
        self.assertEqual(Tournament.objects.get(pk=1).players.count(), 4)
        self.assertEqual(Tournament.objects.get(pk=1).standings.count(), 4)  # type: ignore
        self.assertEqual(Tournament.objects.get(pk=1).rounds.count(), 1)  # type: ignore
        self.assertEqual(Round.objects.get(pk=1).pairings.count(), 2)  # type: ignore
        self.assertEqual(OpponentsTracker.objects.count(), 4)

    def test_tournament_creation_with_odd_number_of_players(self):
        """
        Shouldn't be necessary to repeat all assertions from the test with
        event amount of players since the only difference is the presence of
        the placeholder player for byes.
        """
        response = self.client.post(
            self.url,
            json.dumps(TOURNAMENT_WITH_ODD_NUMBER_OF_PLAYERS),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tournament.objects.count(), 1)
        self.assertEqual(
            Tournament.objects.get(pk=response.json()["id"]).players.count(), 6
        )
        first_round: Round = Tournament.objects.get(pk=1).rounds.get_queryset()[0]  # type: ignore
        self.assertEqual(first_round.pairings.count(), 3)  # type: ignore
