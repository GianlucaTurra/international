from django.db import models


class Player(models.Model):
    name = models.CharField(blank=False, max_length=50)
    is_placeholder = models.BooleanField(default=False)

    class Meta:
        db_table = "players"
        verbose_name_plural = "players"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name
