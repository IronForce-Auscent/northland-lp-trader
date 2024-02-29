from django.urls import path

from . import views

app_name = "lp_trader"
urlpatterns = [
    path("", views.index, name="index"),
    path("auth/login", views.login, name="login"),
    path("auth/update/warning", views.force_update_warning, name="force_update_warning"),
    path("auth/update/force", views.force_update, name="force_update"),
    path("endpoints/update_loyalty", views.update_loyalty, name="update_loyalty"),
    path("endpoints/update_corp_wallet", views.update_corp_wallets, name="update_corp_wallet")
]