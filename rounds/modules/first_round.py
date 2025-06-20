import random
from typing import List

from pairings.models import Pairing, PlayerEntry
from players.models import Player
from rounds.models import Round
from standings.models import Standing
from tournaments.models import Tournament

standings: List[Standing] = []


def generate_first_round(tournament: Tournament) -> None:
    first_round = Round.objects.create(number=1, tournament=tournament)
    player_list = list(tournament.players.all())
    random.shuffle(player_list)
    create_standings(tournament, player_list)
    create_first_round_pairings(first_round, player_list)


def create_first_round_pairings(first_round: Round, player_list: List[Player]):
    """
    Create pairings for the first round of a tournament. With no results nor
    rules to evaluate players the players list is randomly shuffled.
    """
    first_half, second_half = (
        player_list[: len(player_list) // 2],
        player_list[len(player_list) // 2 :],
    )
    pairings: List[Pairing] = []
    players_entries: List[PlayerEntry] = []
    for p1, p2 in zip(first_half, second_half):
        pairing = Pairing(round=first_round)
        pairings.append(pairing)
        players_entries.append(
            PlayerEntry(pairing=pairing, player=p1, standing=find_player_standing(p1))
        )
        players_entries.append(
            PlayerEntry(pairing=pairing, player=p2, standing=find_player_standing(p2))
        )
    Pairing.objects.bulk_create(pairings)
    PlayerEntry.objects.bulk_create(players_entries)


def create_standings(tournament: Tournament, player_list: List[Player]):
    for player in player_list:
        standings.append(Standing(tournament=tournament, player=player))
    Standing.objects.bulk_create(standings)


def find_player_standing(player: Player) -> Standing | None:
    for standing in standings:
        if standing.player is player:
            return standing
