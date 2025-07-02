import json

from django.test import Client, TestCase
from django.urls import reverse_lazy
from test_data import SAVE_FIRST_ROUND_DATA

from pairings.models import Pairing, PlayerEntry
from players.models import Player
from rounds.models import Round
from standings.models import OpponentsTracker, Standing
from tournaments.models import Tournament


class SaveFirstRoundApiTestCase(TestCase):
    def setUp(self) -> None:
        self.tournament = Tournament.objects.create(name="Test")
        # Creating players
        self.timoty = Player.objects.create(name="Timoty")
        self.gianluca = Player.objects.create(name="Gianluca")
        self.edoardo = Player.objects.create(name="Edoardo")
        self.daniele = Player.objects.create(name="Daniele")
        self.tournament.players.add(
            *[self.timoty, self.gianluca, self.edoardo, self.daniele]
        )
        # Creating round and pairings
        self.round = Round.objects.create(number=1, tournament=self.tournament)
        self.pairing_one = Pairing.objects.create(round=self.round)
        self.pairing_two = Pairing.objects.create(round=self.round)
        # Creating standings
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
        # Creatings entries for round
        self.timoty_entry = PlayerEntry.objects.create(
            pairing=self.pairing_one, player=self.timoty, standing=self.timoty_standing
        )
        self.gianluca_entry = PlayerEntry.objects.create(
            pairing=self.pairing_one,
            player=self.gianluca,
            standing=self.gianluca_standing,
        )
        self.eodardo_entry = PlayerEntry.objects.create(
            pairing=self.pairing_two,
            player=self.edoardo,
            standing=self.edoardo_standing,
        )
        self.daniele_entry = PlayerEntry.objects.create(
            pairing=self.pairing_two,
            player=self.daniele,
            standing=self.daniele_standing,
        )
        OpponentsTracker.objects.create(
            standing=self.timoty_standing,
            opponent=self.gianluca_standing,
            round=self.round,
        )
        OpponentsTracker.objects.create(
            standing=self.gianluca_standing,
            opponent=self.timoty_standing,
            round=self.round,
        )
        OpponentsTracker.objects.create(
            standing=self.edoardo_standing,
            opponent=self.daniele_standing,
            round=self.round,
        )
        OpponentsTracker.objects.create(
            standing=self.daniele_standing,
            opponent=self.edoardo_standing,
            round=self.round,
        )
        self.url = reverse_lazy("api-1.0.0:save_round")
        self.client = Client()

    def test_successful_first_round_results(self):
        response = self.client.put(
            self.url, json.dumps(SAVE_FIRST_ROUND_DATA), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.gianluca_standing.refresh_from_db()
        self.timoty_standing.refresh_from_db()
        self.daniele_standing.refresh_from_db()
        self.assertEqual(self.gianluca_standing.matches_played, 1)
        self.assertEqual(self.gianluca_standing.games_won, 2)
        self.assertEqual(self.gianluca_standing.matches_won, 1)
        self.assertEqual(self.gianluca_standing.games_played, 3)
        self.assertGreater(self.gianluca_standing.opponents_game_winrate, 0, 3)
        self.assertEqual(self.timoty_standing.matches_played, 1)
        self.assertEqual(self.timoty_standing.games_won, 1)
        self.assertEqual(self.timoty_standing.matches_won, 0)
        self.assertEqual(self.timoty_standing.games_played, 3)
        self.assertEqual(self.timoty_standing.opponents_match_winrate, 1)
        self.assertEqual(self.daniele_standing.matches_played, 1)
        self.assertEqual(self.daniele_standing.games_won, 2)
        self.assertEqual(self.daniele_standing.matches_won, 1)
        self.assertEqual(self.daniele_standing.games_played, 2)
        self.assertEqual(self.daniele_standing.opponents_game_winrate, 0)

    def test_first_round_results_with_completed_round(self):
        self.round.state = Round.States.COMPLETED
        self.round.save()
        self.round.refresh_from_db()
        response = self.client.put(
            self.url, json.dumps(SAVE_FIRST_ROUND_DATA), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.gianluca_standing.refresh_from_db()
        self.timoty_standing.refresh_from_db()
        self.daniele_standing.refresh_from_db()
        self.assertEqual(self.gianluca_standing.matches_played, 0)
        self.assertEqual(self.gianluca_standing.games_won, 0)
        self.assertEqual(self.gianluca_standing.matches_won, 0)
        self.assertEqual(self.gianluca_standing.games_played, 0)
        self.assertEqual(self.timoty_standing.matches_played, 0)
        self.assertEqual(self.timoty_standing.games_won, 0)
        self.assertEqual(self.timoty_standing.matches_won, 0)
        self.assertEqual(self.timoty_standing.games_played, 0)
        self.assertEqual(self.timoty_standing.opponents_match_winrate, 0)
        self.assertEqual(self.daniele_standing.matches_played, 0)
        self.assertEqual(self.daniele_standing.games_won, 0)
        self.assertEqual(self.daniele_standing.matches_won, 0)
        self.assertEqual(self.daniele_standing.games_played, 0)
        self.assertEqual(self.daniele_standing.opponents_game_winrate, 0)
