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


class UserSerializer(serializers.ModelSerializer):
    #rola_w_aplikacji = RolaWAplikacjiSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('first_name','email')


class TablicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tablica
        fields = '__all__'

class TablicaUzytkownikSerializer(serializers.ModelSerializer):
    #tablica = TablicaSerializer()
    #user = UserSerializer()
    class Meta:
        model = TablicaUzytkownik
        fields = ('tablica','user','rola_w_tablicy')

class TablicaUzytkownicySerializerGET(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = TablicaUzytkownik
        fields = ('tablica','user')

class TablicaUzytkownicySerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = TablicaUzytkownik
        fields = ('tablica','user')

class UzytkownikTabliceSerializerGET(serializers.ModelSerializer):
    tablica = TablicaSerializer()
    class Meta:
        model = TablicaUzytkownik
        fields = ('user','tablica','rola_w_tablicy')

class UzytkownikTabliceSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = TablicaUzytkownik
        fields = ('user','tablica')

class KolumnaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kolumna
        fields = ('tablica','id','tytul')

