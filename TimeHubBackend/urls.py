"""TimeHubBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from RESTApi.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('dj_rest_auth/', include('dj_rest_auth.urls')),
    path('dj_rest_auth/registration/', include('dj_rest_auth.registration.urls')),

    path('api/notatka/', NotatkaViewSetList.as_view()), #MaciekP
    path('api/notatka/<int:pk>/', NotatkaViewSetDetail.as_view()), #MaciekP
    path('api/uzytkownikNotatki/', UzytkownikNotatkiViewSetDetail.as_view()), #MaciekP
    path('api/uzytkownikNotatka/', UzytkownikNotatkaViewSetList.as_view()), #MaciekP



    re_path(r'^api/user/$', UserViewSetList.as_view()),
    re_path(r'^api/user/(?P<pk>[0-9]+)/$', UserViewSetDetail.as_view()),
    re_path(r'^api/tablice/$', TablicaViewSetList.as_view()), #GET i PUT wszystkich tablic
    re_path(r'^api/tablice/(?P<pk>[0-9]+)/$', TablicaViewSetDetail.as_view()), #CRUD do poszczegolnych tablic
    re_path(r'^api/tablicaUzytkownik/$', TablicaUzytkownikViewSetList.as_view()), #Set lista relacji tablica uzytkownik
    re_path(r'^api/tablicaUzytkownicy/(?P<pk>[0-9]+)/$', TablicaUzytkownicyViewSetDetail.as_view()), #wszyscy użytkownicy tablicy okreslonej przez pk , cały CRUD
    re_path(r'^api/uzytkownikTablice/$', UzytkownikTabliceViewSetDetail.as_view()), #tablice danego użytkownika po przekazaniu tokena w headerze requesta

    re_path(r'^api/kolumny/$', KolumnaViewSetList.as_view()), #GET PUT kolumn
    re_path(r'^api/kolumny/(?P<pk>[0-9]+)/$', KolumnaViewSetDetail.as_view()), #Detail set kolumn, GET PUT PATCH DELETE
    re_path(r'^api/tablicaKolumny/(?P<pk>[0-9]+)/$', TablicaKolumnyViewSetDetail.as_view()), #wszystkie kolumny danej tablicy
    re_path(r'^api/kolumnaNotatki/(?P<pk>[0-9]+)/$', KolumnaNotatkiViewSetDetail.as_view()), #wszystkie notatki danej kolumny

    re_path(r'^api/etykiety/$', EtykietaViewSetList.as_view()), #GET PUT etykiet
    re_path(r'^api/etykiety/(?P<pk>[0-9]+)/$', EtykietaViewSetDetail.as_view()), #GET PUT etykiet

    re_path(r'^api/tablicaEtykieta/$', TablicaEtykietaViewSetList.as_view()),
    re_path(r'^api/notatkaEtykieta/$', NotatkaEtykietaViewSetList.as_view()),
    re_path(r'^api/notatkaEtykiety/(?P<pk>[0-9]+)/$', NotatkaEtykietyViewSetDetail.as_view()),
    re_path(r'^api/tabliceEtykiety/(?P<pk>[0-9]+)/$', TablicaEtykietyViewSetDetail.as_view()),

    re_path(r'^api/uzytkownikNotatkiMiesiacRok/$', UzytkownikNotatkiMiesiacRokViewSetDetail.as_view()),
    re_path(r'^api/uzytkownikNotatkiDzienMiesiacRok/$', UzytkownikNotatkiDzienMiesiacRokViewSetDetail.as_view()),
    re_path(r'^api/statystykaNotatkiSkonczoneAktywne7Dni/$',StatystykaNotatkiSkonczoneAktywne7DniViewSetDetail.as_view()),
    re_path(r'^api/statystyka/$',StatystykaProcentowaIloscTaskowWTablicach.as_view()),

]
