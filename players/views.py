from django.http import HttpRequest
from ninja import NinjaAPI, Schema

from players.models import Player, PlayerIn, PlayerOut

api = NinjaAPI()


class Message(Schema):
    message: str


@api.post("create", response={201: PlayerOut, 400: Message})
def create_player(request: HttpRequest, player: PlayerIn):
    if player.id is not None:
        return 400, {"message": "Player already created."}
    p = Player.objects.create(name=player.name)
    return 201, PlayerOut(id=p.pk, name=p.name)
