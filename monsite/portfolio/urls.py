# portfolio/urls.py
from django.urls import path
from django.views.generic.base import RedirectView
from . import views

app_name = 'portfolio'

urlpatterns = [
    # 1) Racine de l’app portfolio : /     ➜ affiche views.accueil
    path('', views.accueil, name='accueil'),
    path("ciscoLabs/", views.cisco_labs, name='cisco-labs'),

    # 2) Ancienne URL “MesPetisCours” qui redirige vers “mes-petits-cours”
    path(
        'MesPetisCours/',
        RedirectView.as_view(pattern_name='portfolio:mespetitscours', permanent=True)
    ),

    # 3) Nouvelle URL “mes-petits-cours”
    path('mes-petits-cours/', views.mesPetitsCours, name='mespetitscours'),

    # 4) Les autres pages statiques
    path('primaire/', views.primaire, name='primaire'),
    path('primaire/cp/', views.cp, name='cp'),
    path('primaire/ce1/', views.ce1, name='ce1'),
    path('primaire/ce2/', views.ce2, name='ce2'),
    path('primaire/cm1/', views.cm1, name='cm1'),
    path('primaire/cm2/', views.cm2, name='cm2'),
    path('project-detail/', views.project_detail, name='project_detail'),
path('projects/concurrency/', views.concurrency, name='concurrency'),
    path('projects/nim-ai/', views.nim_ai, name='nim_ai'),
    path('projects/file-crud/', views.file_crud, name='file_crud'),
    path('projects/javafx-ui/', views.javafx_ui, name='javafx_ui'),
    path('projects/tickethub-ui/', views.tickethub_ui, name='tickethub_ui'),
    path('projects/social-network/', views.social_network, name='social_network'),
    path('projects/secretary-app/', views.secretary_app, name='secretary_app'),
    path('projects/cybersecurity-insights/', views.cybersecurity_insights, name='cybersecurity_insights'),
    path('projects/portfolio-site/', views.portfolio_site, name='portfolio_site'),
    path('projects/task-management/', views.task_management, name='task_management'),
    path('projects/smartbudget-tracker/', views.smartbudget_tracker, name='smartbudget_tracker'),
    path('projects/mailcli-sender/', views.mailcli_sender, name='mailcli_sender'),
    path('projects/taskflow-poo/', views.taskflow_poo, name='taskflow_poo'),
    path('projects/solar-system/', views.solar_system, name='solar_system'),
    path('projects/earthquake-analyzer/', views.earthquake_analyzer, name='earthquake_analyzer'),
    # 5) TicketHub si le voulez accessible depuis portfolio
    path('ticketHub/', views.ticketHub, name='ticketHub'),
]
