from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import Router, Schema
from ninja.pagination import paginate

from players.models import Player, PlayerIn, PlayerOut, players_to_output

router = Router()


class Message(Schema):
    message: str


@router.get("/", response=list[PlayerOut])
@paginate
def get_players(request: HttpRequest):
    return players_to_output(list(Player.objects.all()))


@router.post("/create", response={201: PlayerOut, 400: Message})
def create_player(request: HttpRequest, player: PlayerIn):
    p = Player.objects.create(name=player.name)
    return 201, PlayerOut(id=p.pk, name=p.name)


@router.post("/create-multiple", response={201: list[PlayerOut]})
def create_players(request: HttpRequest, players: list[PlayerIn]):
    ret_players: list[PlayerOut] = []
    for player in players:
        p = Player.objects.create(name=player.name)
        ret_players.append(PlayerOut(id=p.pk, name=p.name))
    return 201, ret_players


@router.get("/{id}")
def get_player(request: HttpRequest, id: int):
    player = get_object_or_404(Player, pk=id)
    return PlayerOut(id=player.pk, name=player.pk)
