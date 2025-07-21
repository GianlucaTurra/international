import math

from django.db import models
from django_extensions.db.models import TimeStampedModel

from players.models import Player
from players.schemas import PlayerIn
from tournaments.exceptions import TournamentIsCompleted, TournamentIsOngoing


class Tournament(TimeStampedModel, models.Model):
    """
    Model representation for a Tournament.
    """

    class States(models.TextChoices):
        PROGRAMMED = "P", "Programmed"
        ONGOING = "O", "Ongoing"
        COMPLETED = "C", "Completed"

    class Types(models.TextChoices):
        SIMPLE = "S", "Simple"

    name = models.CharField(max_length=100)
    players = models.ManyToManyField(Player, related_name="tournaments")
    number_of_rounds = models.IntegerField(null=True)
    state = models.CharField(choices=States, default=States.PROGRAMMED)
    type = models.CharField(choices=Types, default=Types.SIMPLE)

    class Meta:
        """
        Meta information for Tournament table.
        """

        db_table = "tournaments"
        verbose_name_plural = "tournaments"
        get_latest_by = "-created"
        ordering = ("-created",)

    def __str__(self) -> str:
        return self.name

    def is_completed(self) -> bool:
        return self.state == Tournament.States.COMPLETED.value

    def is_ongoing(self) -> bool:
        return self.state == Tournament.States.ONGOING.value

    def add_player_from_playerin_list(self, players: list[PlayerIn] | None):
        if players is None or players == []:
            return
        registered_players: list[Player] = []
        new_players: list[Player] = []
        for player in players:
            if player.id is None:
                p = Player(name=player.name)
                registered_players.append(p)
                new_players.append(p)
            else:
                try:
                    p = Player.objects.get(pk=player.id)
                    registered_players.append(p)
                except Player.DoesNotExist:
                    p = Player(name=player.name)
                    registered_players.append(p)
                    new_players.append(p)
        Player.objects.bulk_create(new_players)
        self.players.add(*registered_players)

    def calculate_optimal_number_of_rounds(self) -> None:
        if self.players.count() <= 0:
            self.number_of_rounds = 1
            return
        self.number_of_rounds = math.ceil(math.log(self.players.count(), 2))

    def start(self) -> None:
        if self.is_completed():
            raise TournamentIsCompleted("Cannot start an already completed tournament")
        if self.is_ongoing():
            raise TournamentIsOngoing("Cannot start and already ongoing tournament")
        self.state = self.States.ONGOING
        self.calculate_optimal_number_of_rounds()
        if (self.players.count() % 2) != 0:
            self.players.add(
                Player.objects.create(name=("Bye - " + self.name), is_placeholder=True)
            )
        self.save()
