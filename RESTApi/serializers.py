from .models import *
from rest_framework import serializers


class NotatkaSerializer(serializers.ModelSerializer): #MaciekP
    class Meta:
        model = Notatka
        fields = ('id', 'stworzone_przez', 'data_stworzenia', 'czy_zrobione', 'czy_wazne', 'zawartosc', 'data_rozpoczecia', 'data_zakonczenia', 'kolumna', 'etykieta')


class RolaWAplikacjiSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolaWAplikacji
        fields = ('__all__')


class UzytkownikSerializer(serializers.ModelSerializer):
    rola_w_aplikacji = RolaWAplikacjiSerializer(read_only=True)

    class Meta:
        model = Uzytkownik
        fields = ('id', 'email', 'haslo', 'zdjecie', 'rola_w_aplikacji')


class TablicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tablica
        fields = '__all__'

class TablicaUzytkownikSerializer(serializers.ModelSerializer):
    tablica = TablicaSerializer()
    uzytkownik = UzytkownikSerializer()
    class Meta:
        model = TablicaUzytkownik
        fields = ('tablica','uzytkownik','rola_w_tablicy')

class TablicaUzytkownicySerializer(serializers.ModelSerializer):
    #uzytkownik = UzytkownikSerializer()
    class Meta:
        model = TablicaUzytkownik
        fields = ('tablica','uzytkownik')

class UzytkownikTabliceSerializer(serializers.ModelSerializer):
    tablica = TablicaSerializer()
    class Meta:
        model = TablicaUzytkownik
        fields = ('uzytkownik','tablica','rola_w_tablicy')
