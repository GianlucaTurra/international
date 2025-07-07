from django.test import TestCase

from standings.models import OpponentsTracker
from pairings.schemas import PairingSchema, PlayerEntrySchema
from players.schemas import PlayerIn, PlayerOut
from rounds.modules.save_round import SimpleSwissRoundSaver
from rounds.schemas import RoundSchema
from tournaments.models import Tournament
from rounds.modules.first_round import RandomFirstRoundGenerator


class CleanOpponentsTrackersAtEndOfTournament(TestCase):
    def setUp(self) -> None:
        self.tournament = Tournament.objects.create(name="test")
        players = [
            PlayerIn(name="Timmy"),
            PlayerIn(name="Dani5"),
        ]
        self.tournament.add_player_from_playerin_list(players)
        self.tournament.number_of_rounds = 1

    def test_all_trackers_are_deleted(self):
        current_round = RandomFirstRoundGenerator(self.tournament).generate()
        entries = [
            PlayerEntrySchema(
                id=1,
                player=PlayerOut(id=1, name="Timmy", is_placeholder=False),
                wins=1,
                draws=0,
            ),
            PlayerEntrySchema(
                id=2,
                player=PlayerOut(id=2, name="Dani5", is_placeholder=False),
                wins=2,
                draws=0,
            ),
        ]
        pairings = PairingSchema(id=1, entries=entries)
        round_results = RoundSchema(id=1, number=1, pairings=[pairings])
        self.assertEqual(OpponentsTracker.objects.count(), 2)
        SimpleSwissRoundSaver(round=round_results, current_round=current_round).save()  # type: ignore
        self.assertEqual(OpponentsTracker.objects.count(), 0)
