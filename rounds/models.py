from django.db import models

from tournaments.models import Tournament


class Round(models.Model):
    """Model definition for Round."""

    number = models.IntegerField()
    tournament = models.ForeignKey(
        Tournament, on_delete=models.CASCADE, related_name="rounds"
    )

    class Meta:
        """Meta definition for Round."""

        db_table = "rounds"
        verbose_name = "Round"
        verbose_name_plural = "Rounds"

    def __str__(self):
        """Unicode representation of Round."""
        return f"Round n.{self.number}"
