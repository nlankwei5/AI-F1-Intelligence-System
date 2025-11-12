from rest_framework import serializers
from .models import *


class analytics_and_prediction_serializer(serializers.ModelSerializer):
    class Meta: 
        model = analytics_and_prediction
        fields = '__all__'

