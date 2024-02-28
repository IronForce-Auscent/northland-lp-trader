from django.urls import path

from . import views

app_name = "lp_trader"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login")
]