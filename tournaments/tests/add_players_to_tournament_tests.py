import json
from django.test import TestCase, Client
from django.urls import reverse_lazy

from players.models import Player
from tournaments.models import Tournament


class AddPlayersToTournamentTestCase(TestCase):
    def setUp(self) -> None:
        self.tournament = Tournament.objects.create(name="Test")
        self.url = reverse_lazy(
            "api-1.0.0:add_players_to_tournament", kwargs={"id": self.tournament.pk}
        )
        self.client = Client()

    def test_without_body(self):
        response = self.client.put(self.url)
        self.assertGreaterEqual(response.status_code, 400)

    def test_wrong_request_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_two_existing_players(self):
        p1 = Player.objects.create(name="Roborbio")
        p2 = Player.objects.create(name="Sgagne")
        response = self.client.put(
            self.url,
            json.dumps(
                [{"id": p1.pk, "name": p1.name}, {"id": p2.pk, "name": p2.name}]
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.tournament.players.count(), 2)

    def test_one_existing_and_one_not(self):
        p1 = Player.objects.create(name="Roborbio")
        response = self.client.put(
            self.url,
            json.dumps([{"id": p1.pk, "name": p1.name}, {"name": "Gnagne"}]),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.tournament.players.count(), 2)
