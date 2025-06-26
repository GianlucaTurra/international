from typing import List

from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from players.models import Player
from players.schemas import PlayerOut, PlayerIn

router = Router()


@router.get("/", response=list[PlayerOut])
@paginate
def get_players(request: HttpRequest):
    return Player.objects.all()


@router.post("/create", response={201: PlayerOut})
def create_player(request: HttpRequest, player: PlayerIn):
    p = Player.objects.create(name=player.name)
    return 201, p


@router.post("/create-multiple", response={201: List[PlayerOut]})
def create_players(request: HttpRequest, players: List[PlayerIn]):
    ret_players: List[Player] = []
    for player in players:
        ret_players.append(Player(name=player.name))
    Player.objects.bulk_create(ret_players)
    return 201, ret_players


@router.get("/{id}")
def get_player(request: HttpRequest, id: int):
    return get_object_or_404(Player, pk=id)
