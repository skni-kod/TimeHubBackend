from django.db import models
from django.contrib.auth.models import User


class ZdjecieUzytkownika(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    zdjecie = models.ImageField(upload_to='zdjecia/')

    def __str__(self):
        return self.user.username


class Tablica(models.Model):
    tytul = models.CharField(max_length=255)
    czy_zautomatyzowane = models.BooleanField(default=False)

    def __str__(self):
        return self.tytul

class TablicaUzytkownik(models.Model):
    tablica = models.ForeignKey(Tablica, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rola_w_tablicy = models.CharField(max_length=255)

    def __str__(self):
        return str(self.tablica)+" "+str(self.user)

class Kolumna(models.Model):
    tytul = models.CharField(max_length=255)
    tablica = models.ForeignKey(Tablica, on_delete=models.CASCADE)

    def __str__(self):
        return self.tytul


class Notatka(models.Model): # MaciekP
    stworzone_przez = models.ForeignKey(User, on_delete=models.CASCADE)
    przypisany_uzytkownik = models.ManyToManyField(User, related_name='przypisany_uzytkownik')
    data_stworzenia = models.DateTimeField(auto_now_add=True)
    czy_zrobione = models.BooleanField(default=False)
    czy_wazne = models.BooleanField(default=False)
    zawartosc = models.TextField()
    data_rozpoczecia = models.DateTimeField(blank=True, null=True)
    data_zakonczenia = models.DateTimeField(blank=True, null=True)
    kolumna = models.ForeignKey(Kolumna, on_delete=models.CASCADE)
    etykieta = models.ManyToManyField('Etykieta')

    def __str__(self):
        return self.zawartosc


class Etykieta(models.Model):
    nazwa = models.CharField(max_length=255)
    opis = models.TextField()
    kolor = models.CharField(max_length=255)
    priorytet = models.IntegerField()

    def __str__(self):
        return self.nazwa


class Zdjecie(models.Model):
    zdjecie = models.ImageField(upload_to='images')
    notatka = models.ForeignKey(Notatka, on_delete=models.CASCADE)

    def __str__(self):
        return self.notatka.zawartosc