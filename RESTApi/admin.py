from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(ZdjecieUzytkownika)
admin.site.register(Tablica)
admin.site.register(Kolumna)
admin.site.register(Notatka)
admin.site.register(Etykieta)
admin.site.register(Zdjecie)
admin.site.register(UzytkownikNotatka)
admin.site.register(TablicaUzytkownik)
admin.site.register(TablicaEtykieta)
admin.site.register(NotatkaEtykieta)

