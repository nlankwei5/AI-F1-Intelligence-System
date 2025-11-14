from django.contrib import admin
from .models import analytics_and_prediction

# Register your models here.

@admin.register(analytics_and_prediction)
class AnalyticsAdmin(admin.ModelAdmin):
    list_display = [
        'ai_response', 
        'status',
        'created_at',
    ]

    list_filter = [
        'created_at', 
        'status'
    ]

    list_per_page = 50
