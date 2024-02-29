from django.contrib import messages
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from esi.decorators import token_required
from esi.models import Token
from esi.managers import TokenQueryset

from .backend import core, endpoints
from .models import CharacterWallet
from northland.northland.settings import ESI_SCOPES

# Create your views here.
def index(request):
    return render(request, "lp_trader/index.html")

@token_required(new=True, scopes=ESI_SCOPES)
def login(request, token):
    core.update_character_db(token)
    return HttpResponseRedirect(reverse("lp_trader:index"))


def force_update_warning(request):
    return render(request, "lp_trader/force_update.html")

def force_update(request):
    tokens = Token.objects.all()
    for token in tokens:
        core.update_character_db(token, force=True)
    return HttpResponseRedirect(reverse("lp_trader:index"))

def update_loyalty(request):
    characters = CharacterWallet.objects.filter(pull_data=True)
    for character in characters:
        messages.success(request, f"{character.char_name}: {character.loyalty_points}")
    return HttpResponseRedirect(reverse("lp_trader:index"))

"""def update_loyalty(request):
    tokens = TokenQueryset(Token).require_scopes("esi-characters.read_loyalty.v1")
    for token in tokens:
        response = endpoints.get_loyalty_points(token, True)
        if response:
            messages.success(request, f"{token.character_name}: {response}")
    return HttpResponseRedirect(reverse("lp_trader:index"))"""

def update_corp_wallets(request):
    token = TokenQueryset(Token).require_scopes(["esi-wallet.read_corporation_wallets.v1", "esi-corporations.read_divisions.v1"])[0]
    response = endpoints.get_corporation_wallet_balance(token)
    if response:
        messages.success(request, response)
    return HttpResponseRedirect(reverse("lp_trader:index"))