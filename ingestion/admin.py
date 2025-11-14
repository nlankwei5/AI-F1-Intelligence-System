from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(EventLog)

@admin.register(TelemetryData)
class TelemetryAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'driver_name', 
        'team', 
        'lap', 
        'speed',
        'gear',
        'rpm',
        'drs',
        'weather', 
        'tyre',
        'session_type',
        'session_id'
    ]

    list_filter = [
        'lap',
        'drs', 
        'circuit_name'
    ]

    search_fields = [
        'circuit_name',
        'session_id'
    ]

    ordering = ['session_id', 'lap', 'id']

    list_per_page = 50