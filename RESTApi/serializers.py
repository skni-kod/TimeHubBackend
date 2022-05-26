from .models import *
from rest_framework import serializers


class NotatkaSerializer(serializers.ModelSerializer): #MaciekP
    class Meta:
        model = Notatka
        fields = ('id', 'stworzone_przez', 'data_stworzenia', 'czy_zrobione', 'czy_wazne', 'zawartosc', 'data_rozpoczecia', 'data_zakonczenia', 'kolumna', 'etykieta')