from typing import Annotated, List, Optional

from ninja import Schema
from pydantic import AfterValidator, ValidationError

from pairings.schemas import PairingSchema
from rounds.models import Round


def exists(id) -> int:
    try:
        return Round.objects.get(pk=id).pk
    except Round.DoesNotExist:
        raise ValidationError(f"Round id {id} does not exists")


class RoundSchema(Schema):
    id: Annotated[int, AfterValidator(exists)]
    number: Optional[int] = None
    pairings: List[PairingSchema]
