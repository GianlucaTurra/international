from django.contrib.auth.password_validation import password_changed

from authentication.models import Token
from .authentication import AuthBearer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpRequest
from ninja.router import Router
from ninja import Schema
from pydantic_core.core_schema import url_schema

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
    first_name: str | None = None
    last_name: str | None = None


class AuhtenticationIn(Schema):
    username: str
    password: str


@router.post("/create-user", response={201: UserOut})
def create_user(request: HttpRequest, payload: UserIn):
    if not payload.first_name:
        payload.first_name = ""
    if not payload.last_name:
        payload.last_name = ""
    return User.objects.create_user(
        username=payload.username,
        password=payload.password,
        email=payload.email,
        first_name=payload.first_name,
        last_name=payload.last_name,
    )


@router.post("/bearer", auth=AuthBearer())
def bearer(request, payload: AuhtenticationIn):
    user = authenticate(username=payload.username, password=payload.password)
    if user:
        token = Token.objects.get_or_create(user=user)
        return 201, {"token": token}
    else:
        return 401, {"error": "invalid credentails"}


# TODO: These methods are almost surely meant for a classic Django applicaiton
# whereas this is meant to be a RESTful API backend and a BrearerToken should be prefered.


# TODO: decide how to handle this and/or login
@router.post("/authenticate-user", response={200: UserOut})
def authenticate_user(request: HttpRequest, payload: AuhtenticationIn):
    return authenticate(useranme=payload.username, password=payload.password)


@router.post("/login", response={200: UserOut})
def login_user(request: HttpRequest, payload: AuhtenticationIn):
    user = authenticate(useranme=payload.username, password=payload.password)
    login(request=request, user=user)
    return user


@router.delete("/logout")
def logout_user(request: HttpRequest):
    logout(request)
