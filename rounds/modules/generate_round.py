from typing import List, Set

from django.db import transaction

from pairings.models import Pairing, PlayerEntry
from rounds.models import Round
from standings.models import Standing
from tournaments.models import Tournament, TournamentIsCompleted


def generate_round(tournament: Tournament) -> Round:
    if tournament.state == Tournament.States.COMPLETED:
        raise TournamentIsCompleted("Cannot create rounds for completed tournaments.")
    round_number = tournament.rounds.count() + 1  # type: ignore
    new_round = Round(
        number=round_number,
        tournament=tournament,
        state=Round.States.ONGOING,
    )
    standings: List[Standing] = list(tournament.standings.all())  # type: ignore
    pairings: List[Pairing] = []
    player_entries: List[PlayerEntry] = []
    while len(standings) > 0:
        standing = standings[0]
        new_opponent: Standing
        opponents_already_faced: Set[Standing] = set(standing.opponents.all())  # type: ignore
        for s in standings[1:]:
            if s in opponents_already_faced:
                continue
            new_opponent = s
            break
        pairing = Pairing(round=new_round)
        entry_1 = PlayerEntry(
            pairing=pairing, player=standing.player, standing=standing
        )
        entry_2 = PlayerEntry(
            pairing=pairing,
            player=new_opponent.player,  # type: ignore
            standing=new_opponent,  # type: ignore
        )
        pairings.append(pairing)
        player_entries.append(entry_1)
        player_entries.append(entry_2)
        standings.pop(0)
        standings.pop(standings.index(new_opponent))  # type: ignore
    with transaction.atomic():
        new_round.save()
        Standing.objects.bulk_create(standings)
        Pairing.objects.bulk_create(pairings)
        PlayerEntry.objects.bulk_create(player_entries)
    return new_round
