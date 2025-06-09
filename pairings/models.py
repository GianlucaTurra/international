from django.db import models

from players.models import Player
from rounds.models import Round


# TODO: questa struttura ha senso?
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


# TODO: il nome fa cahà
class PlayerEntry(models.Model):
    """Model definition for PlayerEntry."""

    pairing = models.ForeignKey(
        Pairing, on_delete=models.CASCADE, related_name="entries"
    )
    player = models.ForeignKey(
        Player, on_delete=models.DO_NOTHING, related_name="pairings"
    )  # TODO: chiarire se può andare bene o meno
    wins = models.IntegerField(default=0)

    class Meta:
        """Meta definition for PlayerEntry."""

        db_table = "player_pairings"
        verbose_name = "Pairing"
        verbose_name_plural = "Pairings"

    def __str__(self):
        return f"{self.player.name} - {self.wins}"
