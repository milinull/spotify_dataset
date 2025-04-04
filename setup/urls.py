from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api_charts.views import SpotifyChartViewSet  # Importe sua View!

router = routers.DefaultRouter()
router.register(r'spotify-charts', SpotifyChartViewSet, basename='spotifychart')  # 🔥 REGISTRE A VIEW!

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Melhor usar 'api/' para organização
]
