# monsite/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('portfolio.urls')),  # Lien vers les vues de ton app

]
