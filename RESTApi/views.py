
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.http import Http404
# Create your views here.


class NotatkaViewSetList(APIView): #MaciekP

    def get(self, request, format=None):
        notatki = Notatka.objects.all()
        serializer = NotatkaSerializer(notatki, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = NotatkaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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


class NotatkiUzytownikaViewSetList(APIView): #MaciekP

    def get(self, request, pk, format=None):
        notatki = Notatka.objects.filter(przypisany_uzytkownik=pk)
        serializer = NotatkaSerializer(notatki, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TablicaViewSetList(APIView):
    def get(self, request):
        queryset = Tablica.objects.all()
        serializer = TablicaSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(selfself, request):
        serializer = TablicaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TablicaViewSetDetail(APIView):
    def get_object(self, pk):
        try:
            return Tablica.objects.get(pk=pk)
        except Tablica.DoesNotExist:
            return Response(status = status.HTTP_200_OK)

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

class TablicaUzytkownicyViewSetDetail(APIView):
    def get_object(self, pk):
        try:
            return TablicaUzytkownik.objects.filter(tablica=pk)
        except TablicaUzytkownik.DoesNotExist:
            return Response(status = status.HTTP_200_OK)

    def get(self, request, pk):
        tablicaUzytkownik = self.get_object(pk)
        serializer = TablicaUzytkownicySerializer(tablicaUzytkownik, many=True)
        return Response(data = serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        serializer = TablicaUzytkownicySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UzytkownikTabliceViewSetDetail(APIView):
    def get_object(self, pk):
        try:
            return TablicaUzytkownik.objects.filter(uzytkownik=pk)
        except TablicaUzytkownik.DoesNotExist:
            return Response(status = status.HTTP_200_OK)

    def get(self, request, pk):
        tablicaUzytkownik = self.get_object(pk)
        serializer = UzytkownikTabliceSerializer(tablicaUzytkownik, many=True)
        return Response(data = serializer.data, status=status.HTTP_200_OK)

    #re
    def post(self, request, pk):
        serializer = UzytkownikTabliceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

