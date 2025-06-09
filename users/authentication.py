from django.http import HttpRequest
from ninja.security import HttpBearer

from international.settings import DEBUG


class AuthBearer(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str):
        if DEBUG:
            return token
