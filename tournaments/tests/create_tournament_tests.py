import json
import pytest
import pytest_django

from django.test import Client, TestCase
from django.urls import reverse_lazy

from rounds.models import Round
from tournaments.models import Tournament

TOURNAMENT_WITH_NONE_PLAYERS = {"name": "test"}
TOURNAMENT_WITH_EMPTY_PLAYERS = {"name": "test", "players": []}
TOURNAMENT_WITH_EVEN_NUMBER_OF_PLAYERS = {
    "name": "test",
    "players": [{"name": "Pito"}, {"name": "Gianni del Baretto"}],
}
TOURNAMENT_WITH_ODD_NUMBER_OF_PLAYERS = {
    "name": "test",
    "players": [
        {"name": "Pito"},
        {"name": "Gianni del Baretto"},
        {"name": "Gino"},
    ],
}


class CreateTournamentTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.url = reverse_lazy("api-1.0.0:create_tournament")

    def test_no_body_request(self):
        response = self.client.post(self.url)
        assert response.status_code >= 400

    def test_simple_tournament_creation(self):
        response = self.client.post(
            self.url,
            json.dumps(TOURNAMENT_WITH_NONE_PLAYERS),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tournament.objects.count(), 1)

    def test_tournament_creation_with_new_player(self):
        response = self.client.post(
            self.url,
            json.dumps(TOURNAMENT_WITH_EVEN_NUMBER_OF_PLAYERS),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tournament.objects.count(), 1)

    def test_tournament_creation_with_odd_number_of_players(self):
        response = self.client.post(
            self.url,
            json.dumps(TOURNAMENT_WITH_ODD_NUMBER_OF_PLAYERS),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tournament.objects.count(), 1)
        self.assertEqual(
            Tournament.objects.get(pk=response.json()["id"]).players.count(), 4
        )
        first_round: Round = Tournament.objects.get(pk=1).rounds.get_queryset()[0]  # type: ignore
        self.assertEqual(first_round.pairings.count(), 2)  # type: ignore
