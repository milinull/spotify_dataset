from rest_framework import viewsets, filters
from .models import SpotifyChart
from .serializers import SpotifyChartSerializer
from django_filters.rest_framework import DjangoFilterBackend

class SpotifyChartViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para fornecer endpoints de leitura para Spotify Charts
    """
    queryset = SpotifyChart.objects.all()
    serializer_class = SpotifyChartSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    filterset_fields = ['chart_date', 'position']
    search_fields = ['artist_title']
    ordering_fields = ['id','position', 'streams', 'total_streams']

