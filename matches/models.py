from django.db import models
from rounds.models import Round
from players.models import Player


class Match(models.Model):
    """Model definition for Match."""

    round = models.ForeignKey(Round, related_name="matches", on_delete=models.CASCADE)
    players = models.ManyToManyField(Player, related_name="matches")

    class Meta:
        """Meta definition for Match."""

        verbose_name = "Match"
        verbose_name_plural = "Matches"

    def __str__(self):
        """Unicode representation of Match."""
        return f""
