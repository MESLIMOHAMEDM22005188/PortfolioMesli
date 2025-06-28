# monsite/urls.py  (le routeur principal du projet)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 1) La route /admin/ pour accéder à l’admin Django
    path('admin/', admin.site.urls),

    # 2) Tout ce qui commence par /tickets/ => on bascule sur tickets/urls.py
    #    Exemple : /tickets/        ➜ tickets/urls.py, route vide ''
    #              /tickets/reset/  ➜ tickets/urls.py, route 'reset/'
    path('tickets/', include('tickets.urls', namespace='tickets')),

    # 3) Tout le reste (la racine "/", etc.) => on bascule sur portfolio/urls.py
    #    Exemple : /       ➜ portfolio/urls.py, route vide ''
    #              /primaire/ ➜ portfolio/urls.py, route 'primaire/'
    path('', include('portfolio.urls', namespace='portfolio')),
]
