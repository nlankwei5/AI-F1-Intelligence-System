from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(TelemetryData)
admin.site.register(EventLog)

