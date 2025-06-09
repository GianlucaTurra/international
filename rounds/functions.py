import random

from pairings.models import Pairing, PlayerEntry
from rounds.models import Round
from tournaments.models import Tournament


def generate_first_round(tournament: Tournament) -> None:
    first_round = Round.objects.create(number=1, tournament=tournament)
    player_list = list(tournament.players.all())
    random.shuffle(player_list)
    first_half, second_half = (
        player_list[: len(player_list) // 2],
        player_list[len(player_list) // 2 :],
    )
    for p1, p2 in zip(first_half, second_half):
        pairing = Pairing.objects.create(round=first_round)
        PlayerEntry.objects.create(pairing=pairing, player=p1)
        PlayerEntry.objects.create(pairing=pairing, player=p2)
