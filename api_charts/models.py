from django.db import models

class SpotifyChart(models.Model):
    """
    Modelo para armazenar dados dos charts do Spotify
    """
    position = models.IntegerField()
    change = models.CharField(max_length=10)
    artist_title = models.CharField(max_length=255)
    days = models.IntegerField()
    peak = models.IntegerField()
    multiplier = models.CharField(max_length=20, null=True, blank=True)
    streams = models.BigIntegerField()
    streams_change = models.CharField(max_length=50)
    week_streams = models.BigIntegerField()
    week_streams_change = models.CharField(max_length=50)
    total_streams = models.BigIntegerField()
    chart_date = models.DateField()

    def __str__(self):
        return f"{self.position}. {self.artist_title}"

    class Meta:
        ordering = ['position']
        unique_together = ['position', 'chart_date']