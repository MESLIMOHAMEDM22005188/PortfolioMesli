"""
Root URL configuration.

Routes requests to the appropriate application.
"""

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("tickets/", include("tickets.urls", namespace="tickets")),
    path("", include("portfolio.urls", namespace="portfolio")),
]