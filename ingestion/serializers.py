from rest_framework import serializers
from .models import *



class TelemetryDataSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TelemetryData
        fields = '__all__'



class EventLogSerializer(serializers.ModelSerializer):
    class Meta: 
        model = EventLog
        fields = '__all__'
