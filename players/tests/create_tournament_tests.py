from django.test import Client, TestCase


class CreateTournamentTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_simple_tournament_creation(self):
        pass
