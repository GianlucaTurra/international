import json

from django.test import Client, TestCase
from django.urls import reverse_lazy

from players.models import Player
from tournaments.models import Tournament


class RemovePlayersFromTournamentTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.url = reverse_lazy("api-1.0.0:remove_players", kwargs={"id": 1})
        self.tournamet = Tournament.objects.create(name="Test")
        self.tournamet.players.add(Player.objects.create(name="Roborbio"))
        self.tournamet.players.add(Player.objects.create(name="Robonto"))
        self.tournamet.players.add(Player.objects.create(name="Sgnagne"))

    def test_simple_remove(self):
        response = self.client.patch(
            self.url,
            json.dumps(
                [
                    1,
                ]
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.tournamet.players.count(), 2)
