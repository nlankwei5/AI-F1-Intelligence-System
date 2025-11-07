from django.test import TestCase
from ingestion.models import TelemetryData, EventLog




class TestTelemetryData(TestCase):
    
    def setUp(self):
        self.telemetry = TelemetryData.objects.create(
            driver_name="Lewis Hamilton",
            team="Mercedes",
            circuit_name="Monza",
            speed=305.5,
            throttle=0.95,
            brake=0.0
        )
        
        
    
    def test_telemetry_creation_and_defaults(self):
        telemetry_1 = TelemetryData.objects.get()

        self.assertEqual(telemetry_1.driver_name, "Lewis Hamilton")
        self.assertEqual(telemetry_1.team, "Mercedes")
        self.assertEqual(telemetry_1.circuit_name, "Monza")
        self.assertEqual(telemetry_1.lap, 0)
        self.assertEqual(telemetry_1.gear, 0)
        self.assertEqual(telemetry_1.rpm, 0)

    
    def test_str_representation(self):
        telemetry_1 = TelemetryData.objects.get()

        expected_str = "Lewis Hamilton: Monza - 0"
        self.assertEqual(str(telemetry_1), expected_str)


class TestEventLog(TestCase):

    def setUp(self):
        telemetry = TelemetryData.objects.create(
            driver_name="Lewis Hamilton",
            team="Mercedes",
            circuit_name="Monza",
            speed=305.5,
            throttle=0.95,
            brake=0.0
        )

        event = EventLog.objects.create(
            telemetry=telemetry,
            event_type="lap_start",
            description="Lap 1 started"
        )


    def test_eventlog_creation_and_uuid(self):
        telemetry_1 = TelemetryData.objects.get()
        event_1 = EventLog.objects.get()
        

        self.assertIsNotNone(event_1.id)
        self.assertIsInstance(event_1.id,  type(event_1.id))
        self.assertEqual(event_1.event_type, "lap_start")

    def test_eventlog_str_returns_uuid(self):
        """Ensure __str__ of EventLog returns its UUID string"""

        event = EventLog.objects.create(event_type="session_end")
        self.assertEqual(str(event), str(event.id))

        
    def test_eventlog_cascade_delete(self):

        telemetry_1 = TelemetryData.objects.get()
        EventLog.objects.create(telemetry=telemetry_1, event_type="pit_in")
        EventLog.objects.create(telemetry=telemetry_1, event_type="pit_out")

        EventLog.objects.create(telemetry=None, event_type="session_start")

        telemetry_1.delete()

        linked_logs = EventLog.objects.filter(event_type__in=["pit_in", "pit_out"])
        self.assertEqual(linked_logs.count(), 0)

        unlinked_logs = EventLog.objects.filter(event_type="session_start")
        self.assertEqual(unlinked_logs.count(), 1)
