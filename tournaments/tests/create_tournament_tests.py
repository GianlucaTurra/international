import json

from django.test import Client, TestCase
from django.urls import reverse_lazy

from rounds.models import Round
from tournaments.models import Tournament


class CreateTournamentTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.url = reverse_lazy("api-1.0.0:create_tournament")

    def test_no_body_request(self):
        response = self.client.post(self.url)
        assert response.status_code >= 400

    def test_simple_tournament_creation(self):
        response = self.client.post(
            self.url, json.dumps({"name": "test"}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tournament.objects.count(), 1)

    def test_tournament_creation_with_new_player(self):
        response = self.client.post(
            self.url,
            json.dumps(
                {
                    "name": "test",
                    "players": [{"name": "Pito"}, {"name": "Gianni del Baretto"}],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tournament.objects.count(), 1)
        self.assertEqual(
            Tournament.objects.get(pk=response.json()["id"]).players.count(), 2
        )

    def test_tournament_creation_with_odd_number_of_players(self):
        response = self.client.post(
            self.url,
            json.dumps(
                {
                    "name": "test",
                    "players": [
                        {"name": "Pito"},
                        {"name": "Gianni del Baretto"},
                        {"name": "Gino"},
                    ],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tournament.objects.count(), 1)
        self.assertEqual(
            Tournament.objects.get(pk=response.json()["id"]).players.count(), 4
        )
        first_round: Round = Tournament.objects.get(pk=1).rounds.get_queryset()[0]  # type: ignore
        self.assertEqual(first_round.pairings.count(), 2)  # type: ignore
