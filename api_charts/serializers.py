from rest_framework import serializers
from .models import SpotifyChart

class SpotifyChartSerializer(serializers.ModelSerializer):
    """
    Serializer para converter modelo SpotifyChart em JSON
    """
    class Meta:
        model = SpotifyChart
        fields = '__all__'