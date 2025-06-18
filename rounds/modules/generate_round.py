from pairings.models import Pairing, PlayerEntry
from rounds.models import Round
from standings.models import Standing
from tournaments.models import Tournament, TournamentIsCompleted
from typing import List


def generate_round(tournament: Tournament) -> None:
    if tournament.state == Tournament.States.COMPLETED:
        raise TournamentIsCompleted("Cannot create rounds for completed tournaments.")
    round_number = tournament.rounds.count() + 1  # type: ignore
    new_round = Round.objects.create(number=round_number, tournament=tournament)
    standings: List[Standing] = list(tournament.standings.all())  # type: ignore
    pairings: List[Pairing] = []
    player_entries: List[PlayerEntry] = []
    for i in range(0, len(standings), 2):
        p1 = standings[i].player
        p2 = standings[i + 1].player
        pairing = Pairing.objects.create(round=new_round)
        p1_entry = PlayerEntry.objects.create(
            pairing=pairing, player=p1, standing=standings[i]
        )
        p2_entry = PlayerEntry.objects.create(
            pairing=pairing, player=p2, standing=standings[i + 1]
        )
        pairings.append(pairing)
        player_entries.append(p1_entry)
        player_entries.append(p2_entry)
    Standing.objects.bulk_create(standings)
    PlayerEntry.objects.bulk_create(player_entries)
