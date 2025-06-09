import math
from typing import List

from django.db import models
from django_extensions.db.models import TimeStampedModel
from ninja import Schema

from players.models import Player, PlayerIn, PlayerOut


class TournamentIsCompleted(Exception):
    """
    Custom Exception raised to explicitly tell api methods the operation is
    not valid for completed tournaments.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Tournament(TimeStampedModel, models.Model):
    """
    Model representation for a Tournament.
    """

    class States(models.TextChoices):
        PROGRAMMED = "P", "Programmed"
        ONGOING = "O", "Ongoing"
        COMPLETED = "C", "Completed"

    name = models.CharField(max_length=100, unique=True)
    players = models.ManyToManyField(Player, related_name="tournaments")
    number_of_rounds = models.IntegerField(null=True)
    state = models.CharField(choices=States, default=States.PROGRAMMED)

    class Meta:
        """
        Meta information for Tournament table.
        """

        db_table = "tournaments"
        verbose_name_plural = "tournamens"
        get_latest_by = "-created"
        ordering = ["-created"]

    def __str__(self) -> str:
        return self.name

    # TODO: refactor with less indentation
    def add_player_from_playerin_list(self, players: list[PlayerIn] | None):
        if players is None:
            return
        registered_players: List[Player] = []
        for player in players:
            if player.id is None:
                registered_players.append(Player.objects.create(name=player.name))
            else:
                try:
                    p = Player.objects.get(pk=player.id)
                    registered_players.append(p)
                except Player.DoesNotExist:
                    registered_players.append(Player.objects.create(name=player.name))
        self.players.add(*registered_players)

    def calculate_optimal_number_of_rounds(self) -> None:
        if self.players.count() <= 0:
            self.number_of_rounds = 1
            return
        self.number_of_rounds = math.ceil(math.log(self.players.count(), 2))

    def start(self) -> None:
        if self.state is self.States.COMPLETED:
            raise TournamentIsCompleted("Cannot start an already completed tournament")
        if self.state is self.States.ONGOING:
            return
        self.state = self.States.ONGOING
        self.calculate_optimal_number_of_rounds()
        if (self.players.count() % 2) != 0:
            self.players.add(
                Player.objects.create(name=("Bye - " + self.name), is_placeholder=True)
            )
        self.save()


class TournamnetIn(Schema):
    name: str
    players: list[PlayerIn] | None = None


class TournamentOut(Schema):
    id: int
    name: str
    players: list[PlayerOut] | None = None
