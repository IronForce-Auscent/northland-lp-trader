from django.contrib import messages
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from esi.decorators import token_required, tokens_required
from esi.models import Token
from bravado.exception import HTTPForbidden

from .backend import endpoints

# Create your views here.

def index(request):
    tokens(request)
    return render(request, "lp_trader/index.html")

@token_required(new=True, scopes="esi-characters.read_loyalty.v1")
def login(request, token):
    return HttpResponseRedirect(reverse("lp_trader:index"))


def tokens(request):
    tokens = Token.objects.all()
    for token in tokens:
        try:
            response = endpoints.get_loyalty_points(token, True)
            if response:
                messages.success(request, f"{token.character_name}: {response}")
        except HTTPForbidden as err:
            # I couldn't delete my first ESI token for some reason, so we'll just skip
            pass
    return HttpResponseRedirect(reverse("lp_trader:index"))