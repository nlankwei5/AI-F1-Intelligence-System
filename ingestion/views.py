from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from .task import run_replay_script
from rest_framework.decorators import action
from rest_framework.response import Response



# Create your views here.

class TelemetryDataViewset(viewsets.ReadOnlyModelViewSet):
    queryset = TelemetryData.objects.all().order_by('-time')
    # permission_classes = [YourCustomApiKeyPermission]
    serializer_class = TelemetryDataSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['driver_name', 'team', 'circuit_name']
    ordering_fields = ['time', 'lap', 'speed']


    @action(detail=False, methods=['post'])
    def start_race(self, request):
        run_replay_script.delay()

        return Response (
            {"status": "Race simulation enqueued"},
            status=status.HTTP_202_ACCEPTED
        )



class EventLogViewset(viewsets.ModelViewSet):
    queryset = EventLog.objects.all()
    serializer_class = EventLogSerializer
    lookup_field = 'id'

