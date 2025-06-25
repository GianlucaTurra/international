from django.db import models

from players.models import Player
from rounds.models import Round
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
    matches_tied = models.IntegerField(default=0)
    games_won = models.IntegerField(default=0)
    games_tied = models.IntegerField(default=0)
    matches_played = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)

    # TODO: are these needed?
    opponents_match_winrate = models.FloatField(default=0)
    opponents_game_winrate = models.FloatField(default=0)
    points = models.IntegerField(default=0)

    class Meta:
        """Meta definition for Standing."""

        verbose_name = "Standing"
        verbose_name_plural = "Standings"
        db_table = "standings"
        ordering = [
            "-tournament",
            "-matches_won",
            "-games_won",
            "-opponents_match_winrate",
            "-opponents_game_winrate",
        ]

    def __str__(self):
        """Unicode representation of Standing."""
        return f"{self.player}: {self.matches_won} - {self.games_won} - {self.points}"

    def update_oppoenets_statistics(self):
        pass


class OpponentsTracker(models.Model):
    """Model needed to keep tracker of a player's opponents during a tournament"""

    standing = models.ForeignKey(
        Standing, on_delete=models.CASCADE, related_name="opponents_tacker"
    )
    opponent = models.ForeignKey(
        Standing, on_delete=models.DO_NOTHING, related_name="opponents"
    )
    round = models.ForeignKey(
        Round, on_delete=models.CASCADE, related_name="opponents_trackers"
    )

    class Meta:
        """Meta information"""

        verbose_name = "OpponentsTracker"
        verbose_name_plural = "OpponentsTrackers"
        db_table = "opponents_trackers"
