from django.urls import path
from .views import manager_home_page

app_name = "manager"
urlpatterns = [path("", view=manager_home_page, name="home")]
