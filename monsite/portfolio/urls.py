from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('mes-petits-cours/', views.mesPetitsCours, name='mespetitscours'),
    path('MesPetisCours/', RedirectView.as_view(pattern_name='mespetitscours', permanent=True)),
    # → Nouveau mapping pour Primaire
    path('primaire/', views.primaire, name='primaire'),
    path('primaire/cp/',  views.cp,  name='cp'),
    path('primaire/ce1/', views.ce1, name='ce1'),
    path('primaire/ce2/', views.ce2, name='ce2'),
    path('primaire/cm1/', views.cm1, name='cm1'),
    path('primaire/cm2/', views.cm2, name='cm2'),
]
