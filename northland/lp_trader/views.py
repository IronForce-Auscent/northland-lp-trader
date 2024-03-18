from django.contrib import messages
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from esi.decorators import token_required
from esi.models import Token
from esi.managers import TokenQueryset

from .backend import data, endpoints
from .models import *
from northland.settings import ESI_SCOPES

# Create your views here.
def index(request):
    return render(request, "lp_trader/index.html")

@token_required(new=True, scopes=ESI_SCOPES)
def login(request, token):
    data.update_character_db(token)
    return HttpResponseRedirect(reverse("lp_trader:index"))


def force_update_warning(request):
    return render(request, "lp_trader/force_update.html")

def update_char(request):
    tokens = Token.objects.all()
    for token in tokens:
        data.update_character_db(token, force=True)
    return HttpResponseRedirect(reverse("lp_trader:index"))

def update_item(request):
    data.update_sde()
    return HttpResponseRedirect(reverse("lp_trader:index"))

def view_loyalty(request):
    data.check_for_character_update()
    characters = Character.objects.filter(pull_data=True)
    for character in characters:
        messages.success(request, f"{character.char_name}: {character.loyalty_points}")
    return HttpResponseRedirect(reverse("lp_trader:index"))

def view_corp_wallets(request):
    token = TokenQueryset(Token).require_scopes(["esi-wallet.read_corporation_wallets.v1", "esi-corporations.read_divisions.v1"])[0]
    balances = endpoints.get_corporation_wallet_balance(token)
    _, divisions = endpoints.get_corporation_divisions(token)
    remapped_wallets = {}
    for entry in balances:
        d, b = entry["division"], entry["balance"]
        div_name = divisions[d - 1]["name"]
        remapped_wallets["Master Wallet" if div_name is None else div_name] = b
    messages.success(request, remapped_wallets)
    return HttpResponseRedirect(reverse("lp_trader:index"))