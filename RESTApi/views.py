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
