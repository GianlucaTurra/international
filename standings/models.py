from django.db import models

from players.models import Player
from tournaments.models import Tournament


class Standing(models.Model):
    """Model definition for Standing."""

    tournament = models.ForeignKey(
        Tournament, on_delete=models.CASCADE, related_name="standings"
    )
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="standings"
    )
    matches_won = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    class Meta:
        """Meta definition for Standing."""

        verbose_name = "Standing"
        verbose_name_plural = "Standings"

    def __str__(self):
        """Unicode representation of Standing."""
        return f"{self.player}: {self.matches_won} - {self.games_won} - {self.points}"
