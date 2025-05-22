from django.http import HttpRequest
from ninja import NinjaAPI

from players.models import playersToOutput
from tournaments.models import Tournament, TournamentOut, TournamnetIn

api = NinjaAPI()


@api.post("/create", response=TournamentOut)
def create_tournament(request: HttpRequest, payload: TournamnetIn):
    """
    Create a tournament with an optional list of players. Players can be
    already registered in the database or not, if not they are registered here.
    """
    tournament = Tournament.objects.create(name=payload.name)
    tournament.add_player_from_playerin_list(payload.players)
    return TournamentOut(
        id=tournament.pk,
        name=tournament.name,
        players=playersToOutput(players=list(tournament.players.all())),
    )
