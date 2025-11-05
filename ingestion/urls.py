from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r"TelemetryData", TelemetryDataViewset, basename="telemetry-data")
router.register(r"EventLog", EventLogViewset, basename="eventlog")


url_patterns = router.urls

