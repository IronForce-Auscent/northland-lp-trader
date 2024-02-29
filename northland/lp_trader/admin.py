from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from esi.models import Token

from .models import CharacterWallet, LoyaltyStore

# Register your models here.
try:
    admin.site.register(CharacterWallet)
    admin.site.register(LoyaltyStore)
except AlreadyRegistered as e:
    print("Model already registered, skipping")