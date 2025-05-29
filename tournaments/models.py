from typing import List
from django.db import models
from django_extensions.db.models import TimeStampedModel
from ninja import Schema
from players.models import Player, PlayerIn, PlayerOut


class Tournament(TimeStampedModel, models.Model):
    name = models.CharField(max_length=100, unique=True)
    players = models.ManyToManyField(Player, related_name="tournaments")
    number_of_rounds = models.IntegerField(null=True)
    ongoing = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    class Meta:
        db_table = "tournaments"
        verbose_name_plural = "tournamens"
        get_latest_by = "-created"
        ordering = ["-created"]

    def __str__(self) -> str:
        return self.name

    def add_player_from_playerin_list(self, players: list[PlayerIn] | None):
        if players is None:
            return
        registered_players: List[Player] = []
        for player in players:
            if player.id is None:
                registered_players.append(Player.objects.create(name=player.name))
            else:
                registered_players.append(Player.objects.get(pk=player.id))
        self.players.add(*registered_players)


class TournamnetIn(Schema):
    name: str
    players: list[PlayerIn] | None = None


class TournamentOut(Schema):
    id: int
    name: str
    players: list[PlayerOut] | None = None
