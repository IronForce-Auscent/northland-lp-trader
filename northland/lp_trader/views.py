from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from esi.decorators import token_required

from .backend import endpoints

# Create your views here.

def index(request):
    return render(request, "lp_trader/index.html")

@token_required(new=True, scopes="esi-characters.read_loyalty.v1")
def login(request, token):
    names_to_ids = endpoints.post_names_to_ids([token.__str__().split("-")[0].strip()])
    print(names_to_ids)
    char_id = names_to_ids["characters"][0]["id"]
    response = endpoints.get_loyalty_points(char_id, token)
    print(response)
    return HttpResponseRedirect(reverse("lp_trader:index"))