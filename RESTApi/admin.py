from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import *

admin.site.register([Uzytkownik, RolaWAplikacji, Tablica, TablicaUzytkownik, Kolumna, Notatka, UzytkownikNotatka, Etykieta, TablicaEtykieta, NotatkaEtykieta, Zdjecie])


