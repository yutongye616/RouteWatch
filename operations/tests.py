import json
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from .models import Incident, MaintenanceTicket, Route, ServiceAlert, Vehicle
from .views import get_nyc_road_summary


class RouteWatchViewsTests(TestCase):
    def setUp(self):
        self.route = Route.objects.create(
            code="M42",
            name="Midtown Loop",
            status="delayed",
            description="Service is affected by weather delays.",
        )
        self.vehicle = Vehicle.objects.create(
            vehicle_id="BUS-101",
            route=self.route,
            status="maintenance",
            capacity=40,
        )
        ServiceAlert.objects.create(
            route=self.route,
            title="Weather delay",
            description="Delays on Midtown Loop expected for the next hour.",
            severity="high",
            is_active=True,
        )
        Incident.objects.create(
            route=self.route,
            vehicle=self.vehicle,
            title="Signal issue",
            description="Signal outage near 42nd Street.",
            severity="medium",
            status="open",
        )
        MaintenanceTicket.objects.create(
            route=self.route,
            vehicle=self.vehicle,
            title="Brake inspection",
            description="Perform brake inspection before next route.",
            status="open",
            priority="high",
            assigned_to="Maintenance Crew A",
        )

    @patch("operations.views.fetch_nyc_incidents")
    def test_home_page_renders(self, mock_fetch):
        mock_fetch.return_value = [{
            "title": "Queens crash",
            "location": "Whitestone Expressway",
            "injuries": "2",
            "factor": "Aggressive Driving/Road Rage",
            "status": "open",
            "severity": "medium",
        }]

        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "RouteWatch")
        self.assertContains(response, "Queens crash")
        self.assertContains(response, "Whitestone Expressway")

    @patch("operations.views.fetch_nyc_incidents")
    def test_route_list_page_renders(self, mock_fetch):
        mock_fetch.return_value = [{
            "title": "Queens crash",
            "location": "Whitestone Expressway",
            "injuries": "2",
            "factor": "Aggressive Driving/Road Rage",
            "status": "open",
            "severity": "medium",
        }]

        response = self.client.get(reverse("route_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Queens crash")
        self.assertContains(response, "Whitestone Expressway")

    def test_service_alert_list_page_renders(self):
        response = self.client.get(reverse("service_alert_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Weather delay")
        self.assertContains(response, self.route.code)

    def test_service_alert_create_page_creates_alert(self):
        response = self.client.post(
            reverse("service_alert_create"),
            {
                "route": self.route.id,
                "title": "Signal maintenance",
                "description": "Temporary signal maintenance on 41st street.",
                "severity": "medium",
                "is_active": "on",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ServiceAlert.objects.filter(title="Signal maintenance").exists())

    def test_incident_list_page_renders(self):
        response = self.client.get(reverse("incident_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Signal issue")
        self.assertContains(response, self.route.code)

    def test_incident_create_page_creates_incident(self):
        response = self.client.post(
            reverse("incident_create"),
            {
                "route": self.route.id,
                "vehicle": self.vehicle.id,
                "title": "Door malfunction",
                "description": "Bus door stuck closed on route M42.",
                "severity": "high",
                "status": "open",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Incident.objects.filter(title="Door malfunction").exists())

    def test_maintenance_ticket_list_page_renders(self):
        response = self.client.get(reverse("maintenance_ticket_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brake inspection")
        self.assertContains(response, self.route.code)

    def test_maintenance_ticket_create_page_creates_ticket(self):
        response = self.client.post(
            reverse("maintenance_ticket_create"),
            {
                "route": self.route.id,
                "vehicle": self.vehicle.id,
                "title": "Tire replacement",
                "description": "Replace worn tires before next dispatch.",
                "status": "open",
                "priority": "high",
                "assigned_to": "Crew B",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(MaintenanceTicket.objects.filter(title="Tire replacement").exists())

    @patch("operations.views.urllib.request.urlopen")
    def test_get_nyc_road_summary_reads_live_api(self, mock_urlopen):
        fake_response = type(
            "FakeResponse",
            (),
            {"read": lambda self: json.dumps([{
                "on_street_name": "Whitestone Expressway",
                "number_of_persons_injured": "2",
                "contributing_factor_vehicle_1": "Aggressive Driving/Road Rage",
            }]).encode("utf-8")}
        )
        mock_urlopen.return_value.__enter__.return_value = fake_response()

        summary = get_nyc_road_summary()

        self.assertEqual(summary["location"], "Whitestone Expressway")
        self.assertEqual(summary["injuries"], "2")
        self.assertEqual(summary["factor"], "Aggressive Driving/Road Rage")

    @patch("operations.views.urllib.request.urlopen")
    def test_get_nyc_road_summary_without_data_returns_fallback(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("API down")

        summary = get_nyc_road_summary()

        self.assertEqual(summary["location"], "NYC roadway")
        self.assertEqual(summary["injuries"], "N/A")
        self.assertEqual(summary["factor"], "Public road data unavailable")
