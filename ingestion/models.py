from django.db import models
import uuid 



class TelemetryData(models.Model):
    driver_name = models.CharField(max_length=100)
    team = models.CharField(max_length=50)
    circuit_name = models.CharField(max_length=100)
    lap = models.IntegerField(default=0)
    speed = models.FloatField()
    throttle = models.FloatField()
    brake = models.FloatField()
    gear = models.IntegerField(default=0)
    rpm = models.IntegerField(default=0)
    drs = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)
    session_type = models.CharField(max_length=100, blank=True,  null =True)

    def __str__(self):
        return f"{self.driver_name}: {self.circuit_name} - {self.lap}"

    class Meta:
        indexes = [      
            models.Index(fields=["driver_name"]),       
            models.Index(fields=["team"]),       
            models.Index(fields=["circuit_name"]),       
        ]



class EventLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    telemetry = models.ForeignKey(TelemetryData, on_delete=models.CASCADE, null=True, blank=True)
    event_type = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"
    class Meta:
        ordering = ["-created_at"]