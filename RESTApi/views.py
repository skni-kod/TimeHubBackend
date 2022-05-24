
from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

from RESTApi.serializers import *
from .models import *

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



