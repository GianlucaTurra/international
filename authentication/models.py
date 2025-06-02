import binascii
import os

from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.models import TimeStampedModel


class Token(TimeStampedModel, models.Model):
    """
    Model representation of a user's Authentication Token
    """

    key = models.CharField(max_length=64, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="token")

    class Meta:
        db_table = "tokens"
        db_table_comment = "Authentication token for users"
        verbose_name = "Token"
        verbose_name_plural = "Tokens"

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls) -> str:
        return binascii.hexlify(os.urandom(32)).decode()
