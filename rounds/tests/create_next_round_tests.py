import json

from django.test import Client, TestCase
from django.urls import reverse

from players.models import Player
from rounds.models import Round
from standings.models import OpponentsTracker, Standing
from tournaments.models import Tournament


class CreateSuccessfulSecondRoundTestCase(TestCase):
    def setUp(self) -> None:
        self.tournament = Tournament.objects.create(name="test")
        # Creating players
        self.timmy = Player.objects.create(name="timmy")
        self.gigi = Player.objects.create(name="gigi")
        self.dani = Player.objects.create(name="dani")
        self.edo = Player.objects.create(name="edo")
        self.tournament.players.add(self.timmy, self.gigi, self.dani, self.edo)
        # Creating standings
        self.timmy_s = Standing.objects.create(
            player=self.timmy,
            tournament=self.tournament,
            games_won=1,
            games_played=3,
            opponents_match_winrate=1,
            opponents_game_winrate=0.66,
        )
        self.gigi_s = Standing.objects.create(
            player=self.gigi,
            tournament=self.tournament,
            games_won=2,
            matches_won=1,
            games_played=2,
            matches_played=1,
            opponents_match_winrate=0,
            opponents_game_winrate=0,
        )
        self.dani_s = Standing.objects.create(
            player=self.dani,
            tournament=self.tournament,
            games_won=0,
            games_played=2,
            matches_played=1,
            opponents_match_winrate=1,
            opponents_game_winrate=1,
        )
        self.edo_s = Standing.objects.create(
            player=self.edo,
            tournament=self.tournament,
            games_won=2,
            matches_won=1,
            games_played=3,
            matches_played=1,
            opponents_match_winrate=0,
            opponents_game_winrate=0.33,
        )
        self.client = Client()
        self.url = reverse("api-1.0.0:create_next_round")

    def test_second_round_with_proper_first_round(self):
        self.first_round = Round.objects.create(
            number=1, tournament=self.tournament, state=Round.States.COMPLETED
        )
        OpponentsTracker.objects.create(
            standing=self.timmy_s, opponent=self.edo_s, round=self.first_round
        )
        OpponentsTracker.objects.create(
            standing=self.edo_s, opponent=self.timmy_s, round=self.first_round
        )
        OpponentsTracker.objects.create(
            standing=self.gigi_s, opponent=self.dani_s, round=self.first_round
        )
        OpponentsTracker.objects.create(
            standing=self.dani_s, opponent=self.gigi_s, round=self.first_round
        )
        response = self.client.post(
            self.url, data=json.dumps({"id": 1}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.tournament.rounds.count(), 2)  # type: ignore

    def test_second_round_with_ongoing_first_round(self):
        self.first_round = Round.objects.create(
            number=1, tournament=self.tournament, state=Round.States.ONGOING
        )
        OpponentsTracker.objects.create(
            standing=self.timmy_s, opponent=self.edo_s, round=self.first_round
        )
        OpponentsTracker.objects.create(
            standing=self.edo_s, opponent=self.timmy_s, round=self.first_round
        )
        OpponentsTracker.objects.create(
            standing=self.gigi_s, opponent=self.dani_s, round=self.first_round
        )
        OpponentsTracker.objects.create(
            standing=self.dani_s, opponent=self.gigi_s, round=self.first_round
        )
        response = self.client.post(
            self.url, data=json.dumps({"id": 1}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.tournament.rounds.count(), 1)  # type: ignore

    def test_second_round_with_completed_tournament(self):
        self.tournament.state = Tournament.States.COMPLETED
        self.tournament.save()
        self.tournament.refresh_from_db()
        self.first_round = Round.objects.create(
            number=1, tournament=self.tournament, state=Round.States.ONGOING
        )
        OpponentsTracker.objects.create(
            standing=self.timmy_s, opponent=self.edo_s, round=self.first_round
        )
        OpponentsTracker.objects.create(
            standing=self.edo_s, opponent=self.timmy_s, round=self.first_round
        )
        OpponentsTracker.objects.create(
            standing=self.gigi_s, opponent=self.dani_s, round=self.first_round
        )
        OpponentsTracker.objects.create(
            standing=self.dani_s, opponent=self.gigi_s, round=self.first_round
        )
        response = self.client.post(
            self.url, data=json.dumps({"id": 1}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.tournament.rounds.count(), 1)  # type: ignore
        # Probably not needed but better safe than sorry
        self.tournament.state = Tournament.States.ONGOING
        self.tournament.save()
        self.tournament.refresh_from_db()
