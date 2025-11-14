from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordResetCompleteView
from . import views

app_name = 'tickets'

urlpatterns = [
    # 1) Page de connexion (racine de l’app tickets)
    path('', views.login_view, name='login'),

    # 2) Création d’alerte (optionnel / admin)
    path('admin/create_alert/', views.create_alert, name='create_alert'),

    # 3) Inscription
    path('register/', views.register_view, name='register'),

    # 4) Déconnexion
    path('logout/', LogoutView.as_view(next_page='tickets:login'), name='logout'),

    # 5) Mot de passe oublié (formulaire)
    path('reset/', views.password_reset_request, name='reset'),

    # 6) Page d’affichage du contenu du mail
    path('reset/done/', views.password_reset_email_page, name='password_reset_done'),

    # 7) Lien cliquable (token + uidb64)
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),

    # 8) Confirmation finale (nouveau mot de passe enregistré)
    path(
        'reset/complete/',
        PasswordResetCompleteView.as_view(
            template_name='tickets/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    # 9) Page d’accueil après connexion
    path('home/', views.home, name='home'),

    # 10) Liste des tickets
    path('list/', views.ticket_list, name='ticket_list'),

    # 11) Création d’un ticket
    path('ticket/create/', views.ticket_create, name='ticket_create'),

    # 12) Fermeture d’un ticket (admin uniquement)
    path('close/<int:pk>/', views.ticket_close, name='ticket_close'),

    # 13) Dashboard admin
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # 14) Détail d’un pôle
    path('pole/<int:pole_id>/', views.pole_description, name='pole_description'),
]
