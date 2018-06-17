# -*- coding: utf-8 -*-
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('Baptismes/',views.Baptismes,name = 'baptismes'),
    path('Baptismes/cerca-batejat/',views.Baptismes,name='baptisme cercat'),
    path('cerca-participant/',views.ParticipantEvent,name = 'cerca participant'),
    path('cerca-protagonista/',views.ProtagonistaEvent,name = 'cerca protagonista'),
    path('Baptismes/cerca-apadrinats/',views.Apadrinats,name = 'apadrinats'),
    path('Matrimonis/',views.Matrimonis,name = 'Matrimonis'),
    path('Matrimonis/cerca-matrimonis/',views.Matrimonis,name = 'cerca matrimonis'),
    path('Obituaris/',views.Obituaris,name = 'Obituaris'),
    path('Obituaris/cerca-obituaris/',views.Obituaris,name = 'cerca obituaris'),
    path('<str:nom_llibre>/<int:num_registre>', views.detail, name='detail'),
    path('vida/',views.vida,name='vida'),
    path('Obituaris/statsMortInfants/',views.simpleMortalitatInfantil, name ='Mortalitat Infantil'),
    path('Matrimonis/fillscasats/',views.FillsCasats, name = 'Fills casats')
]
urlpatterns += staticfiles_urlpatterns()