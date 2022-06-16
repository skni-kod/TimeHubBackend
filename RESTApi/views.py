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

import datetime


class NotatkaViewSetList(APIView): #MaciekP

    def get(self, request, format=None):
        notatki = Notatka.objects.all()
        serializer = NotatkaSerializer(notatki, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = NotatkaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_id = serializer.data.get('stworzone_przez')
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
        return Response(data=serializer.data, status=status.HTTP_200_OK)


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

    def get(self, request):
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

    def get(self, request):
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


class KolumnaViewSetList(APIView):

    def get(self, request, format=None):
        user = Kolumna.objects.all()
        serializer = KolumnaSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = TablicaUzytkownikSerializer(data=request.data)
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


