from django.urls import reverse
from django.test import Client, TestCase
from tournaments.models import Tournament
from rounds.models import Round
from players.models import Player
from standings.models import Standing, OpponentsTracker


class CreateNextRoundTestCase(TestCase):
    def setUp(self) -> None:
        self.tournament = Tournament.objects.create(name="test")
        self.timmy = Player.objects.create(name="timmy")
        self.gigi = Player.objects.create(name="gigi")
        self.dani = Player.objects.create(name="dani")
        self.edo = Player.objects.create(name="edo")
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
        self.tournament.players.add(self.timmy, self.gigi, self.dani, self.edo)
        self.first_round = Round.objects.create(number=1, tournament=self.tournament)
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
        self.client = Client()
        self.url = reverse("api-1.0.0:create_next_round", kwargs={"id": 1})

    def test_round_2_creation(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.tournament.rounds.count(), 2)  # type: ignore
