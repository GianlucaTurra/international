from django.test import Client, TestCase
from django.urls import reverse_lazy

from tournaments.models import Tournament


class StartTournamentTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.url = reverse_lazy("api-1.0.0:start_tournament", kwargs={"id": 1})
        self.tournament = Tournament.objects.create(name="Test")

    def test_round_start(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.tournament.state, self.tournament.States.ONGOING)
