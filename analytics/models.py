from django.db import models
from ingestion.models import TelemetryData

# Create your models here.


class analytics_and_prediction(models.Model):
    telemetry = models.OneToOneField(TelemetryData, on_delete=models.CASCADE)
    prompt = models.TextField()
    ai_response = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis for {self.telemetry}"
    

