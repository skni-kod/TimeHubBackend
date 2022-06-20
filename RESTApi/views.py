from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from collections import OrderedDict
from django.http import Http404
from django.utils import dateparse
from rest_framework.authtoken.models import Token
# Create your views here.

from datetime import datetime, timedelta


class NotatkaViewSetList(APIView): #MaciekP

    def get(self, request, format=None):
        notatki = Notatka.objects.all()
        serializer = NotatkaSerializer(notatki, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):



        new_data = {}

        serializer = NotatkaSerializerPOST(data=request.data)
        if serializer.is_valid():
            user = request.user
            user_id = getattr(user, 'id')
            new_data.update(serializer.data)
            new_data.update({'stworzone_przez': user_id})
            serializer = NotatkaSerializer(data=new_data)
            if serializer.is_valid():
                serializer.save()
                notatka_id = serializer.data.get('id')
                UzytkownikNotatkaViewSetList.outerPost(self, {'user': user_id, 'notatka': notatka_id})
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotatkaViewSetDetail(APIView): #MacieKP

    def get_object(self, pk):
        try:
            return Notatka.objects.get(pk=pk)
        except Notatka.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        notatka = self.get_object(pk)
        serializer = NotatkaSerializer(notatka)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        notatka = self.get_object(pk)
        serializer = NotatkaSerializer(notatka, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        notatka = self.get_object(pk)
        serializer = NotatkaSerializer(notatka, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        notatka = self.get_object(pk)
        notatka.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UzytkownikNotatkaViewSetList(APIView):
    def get(self, request):
        queryset = UzytkownikNotatka.objects.all()
        serializer = UzytkownikNotatkaSerializerGET(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UzytkownikNotatkaSerializerPOST(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def outerPost(self, s_data):
        serializer = UzytkownikNotatkaSerializerPOST(data=s_data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UzytkownikNotatkiViewSetDetail(APIView): #MaciekP
    def get_object(self, pk):
        try:
            return UzytkownikNotatka.objects.filter(user=pk)
        except UzytkownikNotatka.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
          
    def get(self, request):
        user = request.user
        UzytkownikNotatka = self.get_object(getattr(user, 'id'))
        serializer = UzytkownikNotatkaSerializerGET(UzytkownikNotatka, many=True)

        processed_date = []

        for record in serializer.data:
            processed_date.append(record['notatka'])

        return Response(data=processed_date, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = UzytkownikNotatkaSerializerPOST(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UzytkownikNotatkiMiesiacRokViewSetDetail(APIView):
    def get_object(self, pk):
        try:
            return UzytkownikNotatka.objects.filter(user=pk)
        except UzytkownikNotatka.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        request_dict = request.data.dict()
        miesiac = request_dict['miesiac']
        rok = request_dict['rok']

        filtered_data = []
        user = request.user

        UzytkownikNotatka = self.get_object(getattr(user, 'id'))
        serializer = UzytkownikNotatkaSerializerGET(UzytkownikNotatka, many=True)

        for record in serializer.data:
            data_rozpoczecia = dateparse.parse_datetime(record['notatka']['data_rozpoczecia'])
            data_zakonczenia = dateparse.parse_datetime(record['notatka']['data_zakonczenia'])

            if (str(data_rozpoczecia.month) == miesiac and str(data_rozpoczecia.year) == rok) or (str(data_zakonczenia.month) == miesiac and str(data_zakonczenia.year) == rok):
                filtered_data.append(record)

        return Response(data=filtered_data, status=status.HTTP_200_OK)

class UzytkownikNotatkiDzienMiesiacRokViewSetDetail(APIView):
    def get_object(self, pk):
        try:
            return UzytkownikNotatka.objects.filter(user=pk)
        except UzytkownikNotatka.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        request_dict = request.data.dict()
        dzien = request_dict['dzien']
        miesiac = request_dict['miesiac']
        rok = request_dict['rok']

        filtered_data = []
        user = request.user

        UzytkownikNotatka = self.get_object(getattr(user, 'id'))
        serializer = UzytkownikNotatkaSerializerGET(UzytkownikNotatka, many=True)

        for record in serializer.data:
            data_rozpoczecia = dateparse.parse_datetime(record['notatka']['data_rozpoczecia'])
            data_zakonczenia = dateparse.parse_datetime(record['notatka']['data_zakonczenia'])

            if (str(data_rozpoczecia.day) == dzien and str(data_rozpoczecia.month) == miesiac and str(data_rozpoczecia.year) == rok) or (str(data_zakonczenia.day) == dzien and str(data_zakonczenia.month) == miesiac and str(data_zakonczenia.year) == rok):
                filtered_data.append(record)

        return Response(data=filtered_data, status=status.HTTP_200_OK)

class ZrobioneNotatkiDzienMiesiacRokViewSetDetail(APIView):
    def get_object(self, pk):  #funkcja służąca do wyszukiwania notatek danego użytkownika o danym id
        try:
            return UzytkownikNotatka.objects.filter(user=pk)
        except UzytkownikNotatka.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        request_dict = request.data.dict() # zapisanie danych z requesta jako dictionary
        dzien = request_dict['dzien'] #wyciągniecie z body requesta wartości dzien
        miesiac = request_dict['miesiac']   #wyciągniecie z body requesta wartości miesiac
        rok = request_dict['rok']   #wyciągniecie z body requesta wartości rok

        counter = 0 #licznik wszystkich notatek z tego dnia
        counter_done = 0 #licznik zrobionych
        filtered_data = [] #tablica która będzie przechowywać przefiltrowane dane
        user = request.user #pobranie aktualnie zalogowanego użytkownika z requesta

        UzytkownikNotatka = self.get_object(getattr(user, 'id')) #przechwycenie wszystkich notatek zalogowanego użytkownika na podstawie jego id z pobranego wcześniej obiektu usera
        serializer = UzytkownikNotatkaSerializerGET(UzytkownikNotatka, many=True) #serializacja przechwyconych danych

        for record in serializer.data: #iteracja po każdej notatce użytkownika
            data_rozpoczecia = dateparse.parse_datetime(record['notatka']['data_rozpoczecia'])#wyciągniecie z rekordu daty rozpoczecia
            data_zakonczenia = dateparse.parse_datetime(record['notatka']['data_zakonczenia']) #wyciągniecie z rekordu daty zakończenia

            if (str(data_rozpoczecia.day) == dzien and str(data_rozpoczecia.month) == miesiac and str(data_rozpoczecia.year) == rok) or (str(data_zakonczenia.day) == dzien and str(data_zakonczenia.month) == miesiac and str(data_zakonczenia.year) == rok): #sprawdzenie czy notatka jest z danego dnia
                counter = counter + 1 #zwiekszenie licznika o 1
                if record['notatka']['czy_zrobione'] == True: #sprawdzenie czy dana notatka jest oznaczona jako zrobiona
                    counter_done = counter_done + 1 #zwiekszenie licznika zrobionych notatek

        filtered_data.append({'ilosc_zrobionych':counter_done}) #dodanie do seta ilości zrobionych notatek
        filtered_data.append({'wszystkich': counter}) #dodanie do seta ilości wszystkich notatek

        return Response(data=filtered_data, status=status.HTTP_200_OK) #zwrócenie danych poprzez response na front

class StatystykaNotatkiSkonczoneAktywne7DniViewSetDetail(APIView):
    def get_object(self, pk): #funkcja służąca do wyszukiwania notatek danego użytkownika o danym id
        try:
            return UzytkownikNotatka.objects.filter(user=pk)
        except UzytkownikNotatka.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user #pobranie aktualnie zalogowanego użytkownika z requesta

        zrobioneCounter = 0; #licznik notatek oznaczonych jako zrobione
        allCounter = 0; #licznik wszystkich notatek

        UzytkownikNotatka = self.get_object(getattr(user, 'id')) #przechwycenie wszystkich notatek zalogowanego użytkownika na podstawie jego id z pobranego wcześniej obiektu usera
        serializer = UzytkownikNotatkaSerializerGET(UzytkownikNotatka, many=True) #serializacja pobranych wyżej danych
        actualDate = datetime.today().date() #pobranie aktualnej daty

        statistics = {} #set do którego będą dodawanie informacje później wysyłane na front

        for record in serializer.data: #iteracja po każdej notatce użytkownika
            data_rozpoczecia = dateparse.parse_datetime(record['notatka']['data_rozpoczecia']).date() #wyciągniecie z rekordu daty rozpoczecia
            data_zakonczenia = dateparse.parse_datetime(record['notatka']['data_zakonczenia']).date() #wyciągniecie z rekordu daty zakończenia
            czy_zrobione = record['notatka']['czy_zrobione'] #wyciągniecie z rekordu informacji czy zrobione

            if ((data_rozpoczecia>=actualDate - timedelta(days=7) and data_rozpoczecia <= actualDate) or (data_zakonczenia>=actualDate - timedelta(days=7) and data_zakonczenia <= actualDate)): #sprawdzanie czy data rozpoczecia lub data zakończenia jest z przedziału ostatnich 7 dni
                allCounter = allCounter + 1 #zwiekszenie licznika wszystkich notatek o 1
                if(czy_zrobione==True): #jeżeli notatka jest oznaczona jako zrobiona to:
                    zrobioneCounter = zrobioneCounter + 1 #zwiekszenie licznika zrobionych notatek;

        statistics.update({"zrobione": zrobioneCounter}) #dodanie do seta ilości zrobionych notatek
        statistics.update({"w_trakcie": allCounter-zrobioneCounter}) #dodanie do seta ilości notatek w trakcie

        return Response(data=statistics, status=status.HTTP_200_OK) #zwrócenie danych poprzez response na front

class UserViewSetList(APIView):
    def get(self, request, format=None):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserViewSetDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status = status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        queryset = self.get_object(pk)
        serializer = UserSerializer(queryset)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TablicaViewSetList(APIView):
    def get(self, request):
        queryset = Tablica.objects.all()
        serializer = TablicaSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TablicaSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user_id = getattr(user, 'id')
            serializer.save()
            tablica_id = serializer.data.get('id')
            TablicaUzytkownikViewSetList.outerPost(self, {'tablica': tablica_id, 'user': user_id, 'rola_w_tablicy': 'admin'})

            czy_zautomatyzowane = serializer.data.get('czy_zautomatyzowane')
            if czy_zautomatyzowane == True:
                KolumnaViewSetList.outerPost(self, {'tablica': tablica_id, 'tytul': 'To do'})
                KolumnaViewSetList.outerPost(self, {'tablica': tablica_id, 'tytul': 'Doing'})
                KolumnaViewSetList.outerPost(self, {'tablica': tablica_id, 'tytul': 'Testing'})
                KolumnaViewSetList.outerPost(self, {'tablica': tablica_id, 'tytul': 'Done'})

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TablicaViewSetDetail(APIView):
    def get_object(self, pk):
        try:
            return Tablica.objects.get(pk=pk)
        except Tablica.DoesNotExist:
            return Response(status = status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        queryset = self.get_object(pk)
        serializer = TablicaSerializer(queryset)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        tablica = self.get_object(pk)
        serializer = TablicaSerializer(tablica, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        tablica = self.get_object(pk)
        tablica.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        tablica = self.get_object(pk)
        serializer = TablicaSerializer(tablica, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TablicaUzytkownikViewSetList(APIView):
    def get(self, request):
        queryset = TablicaUzytkownik.objects.all()
        serializer = TablicaUzytkownikSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TablicaUzytkownikSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def outerPost(self, s_data):
        serializer = TablicaUzytkownikSerializer(data=s_data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TablicaUzytkownicyViewSetDetail(APIView):
    def get_object(self, pk):
        try:
            return TablicaUzytkownik.objects.filter(tablica=pk)
        except TablicaUzytkownik.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        tablicaUzytkownik = self.get_object(pk)
        serializer = TablicaUzytkownicySerializerGET(tablicaUzytkownik, many=True)
        return Response(data = serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        serializer = TablicaUzytkownicySerializerPOST(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        tablicaUzytkownik = self.get_object(pk)
        serializer = TablicaUzytkownicySerializerPOST(tablicaUzytkownik, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        tablicaUzytkownik = self.get_object(pk)
        serializer = TablicaUzytkownicySerializerPOST(tablicaUzytkownik, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        tablicaUzytkownik = self.get_object(pk)
        tablicaUzytkownik.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UzytkownikTabliceViewSetDetail(APIView):
    def get_object(self, pk):
        try:
            return TablicaUzytkownik.objects.filter(user=pk)
        except TablicaUzytkownik.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user = request.user
        tablicaUzytkownik = self.get_object(getattr(user, 'id'))
        serializer = UzytkownikTabliceSerializerGET(tablicaUzytkownik, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UzytkownikTabliceSerializerPOST(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StatystykaProcentowaIloscTaskowWTablicach(APIView):
    def get(selfself, request):
        user = request.user #pobranie aktualnie zalogowanego użytkownika z requesta
        tablicaUzytkownik = TablicaUzytkownik.objects.filter(user=getattr(user, 'id')) #przechwycenie wszystkich rekordów relacji Tablica Uzytkownik o id uzytkownika równym id usera zalogowanego
        serializerTablicaUzytkownik = UzytkownikTabliceSerializerGET(tablicaUzytkownik, many=True) #serializacja przechwyconych danych

        statistict = {} #pusty set do któego dodawane będą dane wyjściowe
        counter = 0 #licznik przechowujący ilość wszystkich notatek

        for tablice in serializerTablicaUzytkownik.data: #iteracja po wszystkich rekordach z wcześniej przefiltrowanych danych
            tablica_id = tablice['tablica']['id']   #przechwycenie id tablicy  danego rekordu
            statistict.update({str(tablice['tablica']['tytul']): 0})    #dodanie do danych wyjściowych kolejnych nazw tablic z licznikiem ustawionym na 0
            tablicaKolumny = Kolumna.objects.filter(tablica=tablica_id) #przefiltrowanie wszystkich kolumn przypisanych do danej tablicy
            serializerTablicaKolumny = KolumnaSerializer(tablicaKolumny, many=True) #serializacja przechwyconych kolumn
            for kolumny in serializerTablicaKolumny.data: #iteracja po każdej kolumnie danej tablicy
                kolumna_id = kolumny['id']  #przechwycenie id kolumny
                kolumnaNotatki = Notatka.objects.filter(kolumna=kolumna_id) #przefiltrowanie wszystkich notatek przypisanych do danej kolumny
                serializerKolumnaNotatki = NotatkaSerializer(kolumnaNotatki, many=True) #serializacja przechwyconych notatek
                for notatka in serializerKolumnaNotatki.data: #iteracja po każdej notatce danej kolumny
                    statistict[str(tablice['tablica']['tytul'])] = statistict[str(tablice['tablica']['tytul'])] + 1 #zwiększenie licznika ilości notatek(tasków) w danej tablicy
                    counter = counter + 1 #zwiekszenie licznika ilości wszystkich notatek o 1

        for key in statistict.keys(): #iteracja po secie przechowującym ilości notatek w danej tablicy
            statistict[key] = round((statistict[key]*100)/counter) #zmienienie wartości liczbowych na wartości procentowe

        return Response(data=statistict, status=status.HTTP_200_OK) #wysłanie responsa z stworzonym setem danych na front


class KolumnaViewSetList(APIView):

    def get(self, request, format=None):
        user = Kolumna.objects.all()
        serializer = KolumnaSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = KolumnaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def outerPost(self, s_data):
        serializer = KolumnaSerializer(data=s_data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class KolumnaViewSetDetail(APIView):
    def get_object(self, pk):
        try:
            return Kolumna.objects.get(pk=pk)
        except Kolumna.DoesNotExist:
            return Response(status = status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        queryset = self.get_object(pk)
        serializer = KolumnaSerializer(queryset)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        kolumna = self.get_object(pk)
        serializer = KolumnaSerializer(kolumna, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        kolumna = self.get_object(pk)
        kolumna.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        kolumna = self.get_object(pk)
        serializer = KolumnaSerializer(kolumna, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TablicaKolumnyViewSetDetail(APIView):
    def get_object(self, pk):
        try:
            return Kolumna.objects.filter(tablica=pk)
        except Kolumna.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        TablicaKolumny = self.get_object(pk)
        serializer = KolumnaSerializer(TablicaKolumny, many=True)
        return Response(data = serializer.data, status=status.HTTP_200_OK)

class KolumnaNotatkiViewSetDetail(APIView):
    def get_object(self, pk):
        try:
            return Notatka.objects.filter(kolumna=pk)
        except Notatka.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        KolumnaNotatki = self.get_object(pk)
        serializer = NotatkaSerializer(KolumnaNotatki, many=True)
        return Response(data = serializer.data, status=status.HTTP_200_OK)

class EtykietaViewSetList(APIView):

    def get(self, request, format=None):
        etykieta = Etykieta.objects.all()
        serializer = EtykietaSerializer(etykieta, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EtykietaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EtykietaViewSetDetail(APIView):
    def get_object(self, pk):
        try:
            return Etykieta.objects.get(pk=pk)
        except Etykieta.DoesNotExist:
            return Response(status = status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        queryset = self.get_object(pk)
        serializer = EtykietaSerializer(queryset)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        etykieta = self.get_object(pk)
        serializer = EtykietaSerializer(etykieta, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        etykieta = self.get_object(pk)
        etykieta.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        etykieta = self.get_object(pk)
        serializer = EtykietaSerializer(etykieta, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotatkaEtykietaViewSetList(APIView):
    def get(self, request):
        queryset = NotatkaEtykieta.objects.all()
        serializer = NotatkaEtykietaSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = NotatkaEtykietaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TablicaEtykietaViewSetList(APIView):
    def get(self, request):
        queryset = TablicaEtykieta.objects.all()
        serializer = TablicaEtykietaSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TablicaEtykietaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotatkaEtykietyViewSetDetail(APIView):
    def get_object(self, pk):
        try:
            return NotatkaEtykieta.objects.filter(notatka=pk)
        except NotatkaEtykieta.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        notatkaEtykiety = self.get_object(pk)
        serializer = NotatkaEtykietySerializerGET(notatkaEtykiety, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        serializer = NotatkaEtykietaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        notatkaEtykiety = self.get_object(pk)
        serializer = NotatkaEtykietaSerializer(notatkaEtykiety, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        notatkaEtykiety = self.get_object(pk)
        serializer = NotatkaEtykietaSerializer(notatkaEtykiety, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        notatkaEtykiety = self.get_object(pk)
        notatkaEtykiety.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TablicaEtykietyViewSetDetail(APIView):

    def get_object(self, pk):
        try:
            return TablicaEtykieta.objects.filter(tablica=pk)
        except TablicaEtykieta.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        tablicaEtykiety = self.get_object(pk)
        serializer = TablicaEtykietySerializerGET(tablicaEtykiety, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        serializer = TablicaEtykietaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        tablicaEtykiety = self.get_object(pk)
        serializer = TablicaEtykietaSerializer(tablicaEtykiety, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        tablicaEtykiety = self.get_object(pk)
        serializer = TablicaEtykietaSerializer(tablicaEtykiety, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        tablicaEtykiety = self.get_object(pk)
        tablicaEtykiety.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


