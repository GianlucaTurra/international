import json
from django.test import Client, TestCase
from django.urls import reverse_lazy

from players.models import Player


class CreatePlayerTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.single_url = reverse_lazy("api-1.0.0:create_player")
        self.multiple_url = reverse_lazy("api-1.0.0:create_players")

    def test_no_body_request(self):
        response = self.client.post(self.single_url)
        assert response.status_code >= 400
        response = self.client.post(self.multiple_url)
        assert response.status_code >= 400

    def test_single_player_creation(self):
        response = self.client.post(
            self.single_url,
            json.dumps({"name": "Roborbio"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Player.objects.count(), 1)

    def test_multiple_player_creation(self):
        response = self.client.post(
            self.multiple_url,
            json.dumps([{"name": "Roborbio"}, {"name": "Sgnagnez"}]),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Player.objects.count(), 2)

    def test_multiple_player_creation_with_one_non_valid(self):
        response = self.client.post(
            self.multiple_url,
            json.dumps([{"name": "Roborbio"}, {"name": None}, {"name": "Sgnagnez"}]),
            content_type="application/json",
        )
        self.assertGreaterEqual(response.status_code, 400)
        self.assertEqual(Player.objects.count(), 0)
