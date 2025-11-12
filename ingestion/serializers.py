from rest_framework import serializers
from .models import *



class TelemetryDataSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TelemetryData
        fields = ['id', 'driver_name', 'circuit_name', 'lap', 'speed', 'throttle', 'brake', 'gear', 'rpm', 'drs', 'session_type', 'time']
        read_only_fields= ['time']


class SimpleTelemetryDataSerializer(serializers.ModelSerializer):
    class Meta: 
        model = TelemetryData
        fields = ['driver_name', 'circuit_name', 'lap']


class EventLogSerializer(serializers.ModelSerializer):
    class Meta: 
        model = EventLog
        fields = '__all__'

