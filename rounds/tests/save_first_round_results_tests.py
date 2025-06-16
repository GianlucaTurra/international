import json

from django.test import Client, TestCase
from django.urls import reverse_lazy

from pairings.models import Pairing, PlayerEntry
from players.models import Player
from rounds.models import Round
from standings.models import Standing
from tournaments.models import Tournament

TEST_DATA = {
    "id": 1,
    "pairings": [
        {
            "id": 1,
            "entries": [
                {"id": 1, "player": {"id": 1, "name": "Timoty"}, "wins": 1},
                {"id": 2, "player": {"id": 2, "name": "Gianluca"}, "wins": 2},
                {"id": 3, "player": {"id": 3, "name": "Edoardo"}, "wins": 0},
                {"id": 4, "player": {"id": 4, "name": "Daniele"}, "wins": 2},
            ],
        }
    ],
}


class SaveFirstRoundResultsTestCase(TestCase):
    def setUp(self) -> None:
        self.tournament = Tournament.objects.create(name="Test")
        self.timoty = Player.objects.create(name="Timoty")
        self.gianluca = Player.objects.create(name="Gianluuca")
        self.edoardo = Player.objects.create(name="Edoardo")
        self.daniele = Player.objects.create(name="Daniele")
        self.tournament.players.add(
            *[self.timoty, self.gianluca, self.edoardo, self.daniele]
        )
        self.round = Round.objects.create(number=1, tournament=self.tournament)
        self.pairing_one = Pairing.objects.create(round=self.round)
        self.pairing_two = Pairing.objects.create(round=self.round)
        self.timoty_entry = PlayerEntry.objects.create(
            pairing=self.pairing_one, player=self.timoty
        )
        self.gianluca_entry = PlayerEntry.objects.create(
            pairing=self.pairing_one, player=self.gianluca
        )
        self.eodardo_entry = PlayerEntry.objects.create(
            pairing=self.pairing_one, player=self.edoardo
        )
        self.daniele_entry = PlayerEntry.objects.create(
            pairing=self.pairing_one, player=self.daniele
        )
        self.timoty_standing = Standing.objects.create(
            tournament=self.tournament, player=self.timoty
        )
        self.gianluca_standing = Standing.objects.create(
            tournament=self.tournament, player=self.gianluca
        )
        self.edoardo_standing = Standing.objects.create(
            tournament=self.tournament, player=self.edoardo
        )
        self.daniele_standing = Standing.objects.create(
            tournament=self.tournament, player=self.daniele
        )
        self.url = reverse_lazy("api-1.0.0:save_round")
        self.client = Client()

    def test_first_round_results(self):
        response = self.client.put(
            self.url, json.dumps(TEST_DATA), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.gianluca.refresh_from_db()
        self.assertEqual(self.gianluca_standing.matches_played, 1)
        self.assertEqual(self.gianluca_standing.matches_won, 1)
