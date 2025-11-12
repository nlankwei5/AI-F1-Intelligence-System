from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter


# Create your views here.

class analytics_and_predictionViewset(viewsets.ReadOnlyModelViewSet):
    queryset = analytics_and_prediction.objects.all().order_by('-time')
    serializer_class = analytics_and_prediction_serializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'status']
