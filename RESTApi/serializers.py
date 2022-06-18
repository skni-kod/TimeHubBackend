from .models import *
from rest_framework import serializers


class NotatkaSerializer(serializers.ModelSerializer): #MaciekP
    class Meta:
        model = Notatka
        fields = ('id', 'kolumna', 'data_stworzenia', 'czy_zrobione', 'czy_wazne', 'zawartosc', 'data_rozpoczecia', 'data_zakonczenia', 'stworzone_przez')

class NotatkaSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = Notatka
        fields = ('id', 'kolumna', 'data_stworzenia', 'czy_zrobione', 'czy_wazne', 'zawartosc', 'data_rozpoczecia', 'data_zakonczenia')

class UzytkownikNotatkaSerializerPOST(serializers.ModelSerializer): #MaciekP
    class Meta:
        model = UzytkownikNotatka
        fields = ('user', 'notatka')

class UzytkownikNotatkaSerializerGET(serializers.ModelSerializer): #MaciekP
    notatka = NotatkaSerializer()
    class Meta:
        model = UzytkownikNotatka
        fields = ('user', 'notatka') 


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name')


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
        fields = ('id','user','tablica')

class KolumnaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kolumna
        fields = ('id','tablica','tytul')

class KolumnaSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = Kolumna
        fields = ('tablica','tytul')

class EtykietaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etykieta
        fields = ('nazwa', 'opis', 'kolor', 'priorytet')

class NotatkaEtykietaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotatkaEtykieta
        fields = ('notatka', 'etykieta')

class NotatkaEtykietySerializerGET(serializers.ModelSerializer):
    etykieta = EtykietaSerializer()
    class Meta:
        model = NotatkaEtykieta
        fields = ('notatka', 'etykieta')

class TablicaEtykietaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TablicaEtykieta
        fields = ('tablica', 'etykieta')

class TablicaEtykietySerializerGET(serializers.ModelSerializer):
    etykieta = EtykietaSerializer()
    class Meta:
        model = TablicaEtykieta
        fields = ('tablica', 'etykieta')
