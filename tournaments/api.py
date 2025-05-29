from typing import List

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from players.models import Player, PlayerIn, PlayerOut
from tournaments.models import Tournament, TournamentOut, TournamnetIn

router = Router()


@router.post("/create", response={201: TournamentOut})
def create_tournament(request: HttpRequest, payload: TournamnetIn):
    """
    Create a tournament with an optional list of players. Players can be
    already registered in the database or not, if not they are registered here.
    """
    tournament = Tournament.objects.create(name=payload.name)
    tournament.add_player_from_playerin_list(payload.players)
    return 201, tournament


@router.get("/{id}", response={200: TournamentOut})
def get_tournament(request: HttpRequest, id: int):
    return get_object_or_404(Tournament, pk=id)


@router.patch("/{id}/players/remove", response=List[PlayerOut])
def remove_players(request: HttpRequest, id: int, players: List[int]):
    """
    Remove a list of players from a given tournaments. If a given id does not
    exist in the Player table or in the tournament's player list it is ignored.
    """
    tournament = get_object_or_404(Tournament, pk=id)
    for player in players:
        p: Player | None = None
        try:
            p = Player.objects.get(pk=player)
        except Player.DoesNotExist:
            continue
        if tournament.players.contains(p):
            tournament.players.remove(p)
    return tournament.players.all()


@router.delete("/{id}", response=TournamentOut)
def delete_tournament(request: HttpRequest, id: int):
    tournament = get_object_or_404(Tournament, pk=id)
    tournament.delete()
    return 200, tournament


@router.put("/{id}/add-players", response=List[PlayerOut])
def add_players_to_tournament(request: HttpRequest, id: int, payload: List[PlayerIn]):
    """
    Add a list of players to a tournament.
    Players without id are registered and added to the tournament.
    Returns the list of registered players to that tournament including
    previously registered players.
    """
    tournament = get_object_or_404(Tournament, pk=id)
    for player in payload:
        if player.id is None:
            p = Player.objects.create(name=player.name)
            tournament.players.add(p)
        try:
            p = Player.objects.get(pk=player.id)
            tournament.players.add(p)
        except Player.DoesNotExist:
            continue
        tournament.players.add()
    return tournament.players.all()


@router.get("/", response=List[TournamentOut])
@paginate
def get_tournaments(request: HttpRequest):
    """
    Get the list of all tournaments.
    """
    return Tournament.objects.all()
