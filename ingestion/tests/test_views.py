from rest_framework.test import APITestCase
from ingestion.models import *
from django.urls import reverse


class TestTelemetryDataViewset(APITestCase):

    def setUp(self):
        """Set up sample data for tests"""
        self.telemetry1 = TelemetryData.objects.create(
            driver_name="Max Verstappen",
            team="Red Bull",
            circuit_name="Spa",
            lap=10,
            speed=320.0,
            throttle=0.9,
            brake=0.1,
        )
        self.telemetry2 = TelemetryData.objects.create(
            driver_name="Lewis Hamilton",
            team="Mercedes",
            circuit_name="Monza",
            lap=12,
            speed=315.0,
            throttle=0.8,
            brake=0.2,
        )


    def test_list_view_returns_all_data(self):
        """GET /telemetry/ should return all records"""
        url = reverse("telemetry-data-list")  
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertIn("driver_name", response.data[0])


    def test_default_ordering(self):
        url = reverse("telemetry-data-list")
        response = self.client.get(url)

        times = [t["time"] for t in response.data]
        self.assertTrue(times[0] >= times[1])

    def test_search_by_driver_name(self):
        """Search should filter by driver_name"""
        url = reverse("telemetry-data-list")
        response = self.client.get(url, {"search": "Lewis"})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["driver_name"], "Lewis Hamilton")

    def test_post_is_forbidden_on_readonly_viewset(self):
        """Ensure write operations are not allowed"""
        url = reverse("telemetry-data-list")
        payload = {"driver_name": "Test Driver"}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 405)


class TestEventLogViewset(APITestCase):

    def setUp(self):
        self.eventlog_url = reverse("eventlog-list")

    def test_create_event_log(self):
        payload = {"event_type": "race_start", "description": "Lights out!"}
        response = self.client.post(self.eventlog_url, payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(EventLog.objects.count(), 1)
        self.assertEqual(EventLog.objects.first().event_type, "race_start")

    def test_retrieve_event_log(self):
        log = EventLog.objects.create(event_type="race_end")
        url = reverse("eventlog-detail", args=[log.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["event_type"], "race_end")

    def test_delete_event_log(self):
        log = EventLog.objects.create(event_type="crash")
        url = reverse("eventlog-detail", args=[log.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(EventLog.objects.count(), 0)