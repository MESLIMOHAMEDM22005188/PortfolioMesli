# tickets/urls.py
from django.urls import path, include
from django.contrib.auth.views import LogoutView, PasswordResetCompleteView
from . import views

app_name = 'tickets'

urlpatterns = [
    # 1) Page de connexion (racine de l’app tickets)
    path('', views.login_view, name='login'),
    path('"admin/create_alert/"', views.create_alert, name='create_alert'),

    # 2) Inscription
    path('register/', views.register_view, name='register'),

    # 3) Déconnexion
    path('logout/', LogoutView.as_view(next_page='tickets:login'), name='logout'),

    # 4) Mot de passe oublié (formulaire)
    path('reset/', views.password_reset_request, name='reset'),

    # 5) Page d’affichage du contenu du mail
    path('reset/done/', views.password_reset_email_page, name='password_reset_done'),

    # 6) Lien cliquable (token + uidb64)
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),

    # 7) Confirmation finale (nouveau mot de passe enregistré)
    path(
        'reset/complete/',
        PasswordResetCompleteView.as_view(
            template_name='tickets/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    # 8) Routes Django standard (change-password, etc.) si besoin
    path('accounts/', include('django.contrib.auth.urls')),

    path('home/', views.home, name='home'),
    # 9) Liste des tickets (après connexion)
    path('list/', views.ticket_list, name='ticket_list'),


    # 11) Fermeture d’un ticket (admin uniquement)
    path('close/<int:pk>/', views.ticket_close, name='ticket_close'),

    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('ticket/create/', views.ticket_create, name='ticket_create'),
    path('pole/<int:pole_id>/', views.pole_description, name='pole_description'),


]
