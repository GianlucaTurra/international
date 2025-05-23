from django.http import HttpRequest
from ninja import NinjaAPI, Schema

from players.models import Player, PlayerIn, PlayerOut

api = NinjaAPI(urls_namespace="players")


class Message(Schema):
    message: str


@api.post("create", response={201: PlayerOut, 400: Message})
def create_player(request: HttpRequest, player: PlayerIn):
    p = Player.objects.create(name=player.name)
    return 201, PlayerOut(id=p.pk, name=p.name)


@api.post("create-multiple", response={201: list[PlayerOut]})
def create_players(request: HttpRequest, players: list[PlayerIn]):
    ret_players: list[PlayerOut] = []
    for player in players:
        p = Player.objects.create(name=player.name)
        ret_players.append(PlayerOut(id=p.pk, name=p.name))
    return 201, ret_players
