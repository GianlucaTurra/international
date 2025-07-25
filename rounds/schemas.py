from typing import Annotated

from ninja import Schema
from pydantic import AfterValidator, ValidationError

from pairings.schemas import PairingSchema
from rounds.models import Round


def exists(id) -> int:
    try:
        return Round.objects.get(pk=id).pk
    except Round.DoesNotExist as e:
        raise ValidationError(f"Round id {id} does not exists") from e


class RoundSchema(Schema):
    id: Annotated[int, AfterValidator(exists)]
    number: int | None = None
    pairings: list[PairingSchema]
