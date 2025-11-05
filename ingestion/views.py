from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter



# Create your views here.

class TelemetryDataViewset(viewsets.ReadOnlyModelViewSet):
    queryset = TelemetryData.objects.all().order_by('-time')
    serializer_class = TelemetryDataSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['driver_name', 'team', 'circuit_name']
    ordering_fields = ['time', 'lap', 'speed']


class EventLogViewset(viewsets.ModelViewSet):
    queryset = EventLog.objects.all()
    serializer_class = EventLogSerializer
    lookup_field = 'id'

