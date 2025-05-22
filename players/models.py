from django.db import models
from ninja import Schema


class Player(models.Model):
    name = models.CharField(blank=False, max_length=50, unique=True)
    is_placeholder = models.BooleanField(default=False)

    class Meta:
        db_table = "players"
        verbose_name_plural = "players"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class PlayerIn(Schema):
    id: int | None = None
    name: str


class PlayerOut(Schema):
    id: int
    name: str


def playersToOutput(players: list[Player]) -> list[PlayerOut]:
    return [PlayerOut(id=player.pk, name=player.name) for player in players]
