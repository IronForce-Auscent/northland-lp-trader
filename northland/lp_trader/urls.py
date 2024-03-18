from django.urls import path

from . import views

app_name = "lp_trader"
urlpatterns = [
    path("", views.index, name="index"),
    path("auth/login", views.login, name="login"),
    path("auth/update/warning", views.force_update_warning, name="update_warning"),
    path("auth/update/char", views.update_char, name="update_char"),
    path("auth/update/item", views.update_item, name="update_item"),
    path("endpoints/get/loyalty", views.view_loyalty, name="view_loyalty"),
    path("endpoints/get/corp_wallet", views.view_corp_wallets, name="view_corp_wallet")
]