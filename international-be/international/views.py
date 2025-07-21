from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse


def redirect_to_manager_app(request: HttpRequest) -> HttpResponse:
    return redirect(reverse("manager:home"))
