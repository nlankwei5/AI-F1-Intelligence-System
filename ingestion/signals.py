from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TelemetryData
from analytics.tasks import analyze_lap_telemetry

@receiver(post_save, sender=TelemetryData)
def trigger_analysis(sender, instance, created, **kwargs):
    if created:
        # Send lap data ID to the analytics worker
        analyze_lap_telemetry.delay(instance.id)
