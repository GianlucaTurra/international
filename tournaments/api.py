from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from players.models import players_to_output
from tournaments.models import Tournament, TournamentOut, TournamnetIn

router = Router()


@router.get("/read/{id}", response=TournamentOut)
def get_tournament(request: HttpRequest, id: int):
    tournament = get_object_or_404(Tournament, pk=id)
    return TournamentOut(id=tournament.pk, name=tournament.name)


@router.get("/all", response=list[TournamentOut])
@paginate
def get_tournaments(request: HttpRequest) -> list[TournamentOut]:
    return [
        TournamentOut(
            id=t.pk, name=t.name, players=players_to_output(list(t.players.all()))
        )
        for t in Tournament.objects.all()
    ]


@router.post("/create", response={201: TournamentOut})
def create_tournament(request: HttpRequest, payload: TournamnetIn):
    """
    Create a tournament with an optional list of players. Players can be
    already registered in the database or not, if not they are registered here.
    """
    tournament = Tournament.objects.create(name=payload.name)
    tournament.add_player_from_playerin_list(payload.players)
    return 201, TournamentOut(
        id=tournament.pk,
        name=tournament.name,
        players=players_to_output(players=list(tournament.players.all())),
    )
