from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from esi.models import Token

from .models import *

# Register your models here.
admin.site.register(Character)
admin.site.register(Corp)
admin.site.register(Item)