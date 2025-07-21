from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def manager_home_page(request: HttpRequest) -> HttpResponse:
    return render(request, "managerapp/home.html")
