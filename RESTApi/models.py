from django.db import models
from django.contrib.auth.models import User

class RolaWAplikacji(models.Model):
    nazwa = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.nazwa)

class Uzytkownik(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    haslo = models.CharField(max_length=255)
    zdjecie = models.ImageField(upload_to='profile_pics', blank=True)
    rola_w_aplikacji = models.ForeignKey(RolaWAplikacji, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.email)


class Tablica(models.Model):
    tytul = models.CharField(max_length=255)
    czy_zautomatyzowane = models.BooleanField(default=False)

    def __str__(self):
        return str(self.tytul)

class TablicaUzytkownik(models.Model):
    tablica = models.ForeignKey(Tablica, on_delete=models.CASCADE)
    uzytkownik = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)
    rola_w_tablicy = models.CharField(max_length=255)

    def __str__(self):
        return str(self.tablica)+" "+str(self.uzytkownik)

class Kolumna(models.Model):
    tytul = models.CharField(max_length=255)
    tablica = models.ForeignKey(Tablica, on_delete=models.CASCADE)

class Notatka(models.Model):
    stworzone_przez = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)
    data_stworzenia = models.DateTimeField(auto_now_add=True)
    czy_zrobione = models.BooleanField(default=False)
    czy_wazne = models.BooleanField(default=False)
    zawartosc = models.TextField()
    data_rozpoczecia = models.DateTimeField(blank=True, null=True)
    data_zakonczenia = models.DateTimeField(blank=True, null=True)
    kolumna = models.ForeignKey(Kolumna, on_delete=models.CASCADE)

class UzytkownikNotatka(models.Model):
    uzytkownik = models.ForeignKey(Uzytkownik, on_delete=models.CASCADE)
    notatka = models.ForeignKey(Notatka, on_delete=models.CASCADE)

class Etykieta(models.Model):
    nazwa = models.CharField(max_length=255)
    opis = models.TextField()
    kolor = models.CharField(max_length=255)
    priorytet = models.IntegerField()

class TablicaEtykieta(models.Model):
    tablica = models.ForeignKey(Tablica, on_delete=models.CASCADE)
    etykieta = models.ForeignKey(Etykieta, on_delete=models.CASCADE)

class NotatkaEtykieta(models.Model):
    notatka = models.ForeignKey(Notatka, on_delete=models.CASCADE)
    etykieta = models.ForeignKey(Etykieta, on_delete=models.CASCADE)

class Zdjecie(models.Model):
    zdjecie = models.ImageField(upload_to='images')
    notatka = models.ForeignKey(Notatka, on_delete=models.CASCADE)