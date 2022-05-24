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
from django.urls import path, re_path
from RESTApi.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/tablice/$', TablicaViewSetList.as_view()),
    re_path(r'^api/tablice/(?P<pk>[0-9]+)/$', TablicaViewSetDetail.as_view()),
    re_path(r'^api/tablicaUzytkownik/$', TablicaUzytkownikViewSetList.as_view()),
    re_path(r'^api/tablicaUzytkownicy/(?P<pk>[0-9]+)/$', TablicaUzytkownicyViewSetDetail.as_view()),
    re_path(r'^api/uzytkownikTablice/(?P<pk>[0-9]+)/$', UzytkownikTabliceViewSetDetail.as_view()),
]
