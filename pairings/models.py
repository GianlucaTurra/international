from enum import Enum
from django.db import models
from django.db.models.fields.related import ForeignKey

from players.models import Player
from rounds.models import Round
from standings.models import Standing


class Pairing(models.Model):
    """Model definition for Pairing."""

    round = models.ForeignKey(Round, related_name="pairings", on_delete=models.CASCADE)

    class Meta:
        """Meta definition for Pairings."""

        verbose_name = "Pairing"
        verbose_name_plural = "Pairings"

    def __str__(self):
        """Unicode representation of Pairings."""
        return ""


class PairingResult(Enum):
    WIN = 1
    DRAW = 2
    LOSS = 3


class PlayerEntry(models.Model):
    """
    Model definition to associate a Player to a pairings, tracking his results.
    """

    pairing = models.ForeignKey(
        Pairing, on_delete=models.CASCADE, related_name="entries"
    )
    player: ForeignKey[Player] = models.ForeignKey(
        Player, on_delete=models.DO_NOTHING, related_name="pairings"
    )
    standing: ForeignKey[Standing] = models.ForeignKey(
        Standing, on_delete=models.CASCADE, related_name="pairing_entries", null=True
    )
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)

    class Meta:
        """Meta definition for PlayerEntry."""

        db_table = "player_pairings"
        verbose_name = "Pairing"
        verbose_name_plural = "Pairings"

    def __str__(self):
        return f"{self.player.name} - {self.wins}"

    def update_standings(self, result: PairingResult, games_played: int):
        self.standing.games_won += self.wins
        self.standing.games_tied += self.draws
        self.standing.matches_played += 1
        self.standing.games_played += games_played
        match result:
            case PairingResult.WIN:
                self.standing.matches_won += 1
                self.standing.points += 3
            case PairingResult.DRAW:
                self.standing.matches_tied += 1
                self.standing.points += 1
        self.standing.save()
