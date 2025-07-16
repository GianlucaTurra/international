from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate
from ninja_jwt.authentication import JWTAuth

from international.schemas import ErrorMessage
from rounds.modules.round_manager_factory import get_first_round_generator
from tournaments.exceptions import TournamentIsOngoing
from tournaments.models import Tournament, TournamentIsCompleted
from tournaments.schemas import TournamentOut, TournamnetIn

router = Router()


@router.post(
    "/create",
    auth=JWTAuth(),
    response={201: TournamentOut, 400: ErrorMessage},
)
def create_tournament(request: HttpRequest, payload: TournamnetIn):
    """
    Create a tournament with an optional list of players. Players can be
    already registered in the database or not, if not they are registered here.
    This operation is not valid for ongoing or completed tournaments.
    """
    tournament = Tournament.objects.create(name=payload.name)
    tournament.add_player_from_playerin_list(payload.players)
    try:
        tournament.start()
    except (TournamentIsCompleted, TournamentIsOngoing) as e:
        return ErrorMessage(content=e.message)
    get_first_round_generator(tournament).generate_round()
    return 201, tournament


@router.get("/{id}", response={200: TournamentOut, 404: None})
def get_tournament(request: HttpRequest, id: int):
    """
    Get a tournament by ID. If not found, a 404 response code is given.
    """
    return get_object_or_404(Tournament, pk=id)


@router.delete("/{id}", auth=JWTAuth(), response={200: TournamentOut, 404: None})
def delete_tournament(request: HttpRequest, id: int):
    tournament = get_object_or_404(Tournament, pk=id)
    tournament.delete()
    return 200, tournament


@router.get("/", response={200: list[TournamentOut]})
@paginate
def get_tournaments(request: HttpRequest):
    """
    Get the list of all tournaments.
    """
    return 200, Tournament.objects.all()
