from django.db import models

from tournaments.models import Tournament


class Round(models.Model):
    """Model definition for Round."""

    class States(models.TextChoices):
        PROGRAMMED = "P", "Programmed"
        ONGOING = "O", "Ongoing"
        COMPLETED = "C", "Completed"

    number = models.IntegerField()
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        related_name="rounds",
    )
    state = models.CharField(
        choices=States,
        default=States.PROGRAMMED,
    )

    class Meta:
        """Meta definition for Round."""

        db_table = "rounds"
        verbose_name = "Round"
        verbose_name_plural = "Rounds"
        get_latest_by = "-pk"

    def __str__(self):
        """Unicode representation of Round."""
        return f"Round n.{self.number}"
