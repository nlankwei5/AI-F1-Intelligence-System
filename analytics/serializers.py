from rest_framework import serializers
from .models import *
from ingestion.serializers import SimpleTelemetryDataSerializer


class analytics_and_prediction_serializer(serializers.ModelSerializer):
    telemetry = SimpleTelemetryDataSerializer()
    
    class Meta: 
        model = analytics_and_prediction
        fields = ['telemetry', 'prompt', 'ai_response', 'status', 'created_at']

