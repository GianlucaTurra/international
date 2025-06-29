from typing import Optional

from django.contrib.auth.models import User
from django.http import HttpRequest
from ninja import Schema
from ninja.router import Router

router = Router()


class UserOut(Schema):
    username: str
    email: str
    first_name: str
    last_name: str


class UserIn(Schema):
    username: str
    password: str
    email: str
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""


@router.post("/create-user", response={201: UserOut})
def create_user(request: HttpRequest, payload: UserIn):
    return User.objects.create_user(
        username=payload.username,
        password=payload.password,
        email=payload.email,
        first_name=payload.first_name,
        last_name=payload.last_name,
    )
