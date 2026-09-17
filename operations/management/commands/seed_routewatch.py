from django.core.management.base import BaseCommand

from operations.models import Incident, MaintenanceTicket, Route, ServiceAlert, Vehicle


class Command(BaseCommand):
    help = "Seed RouteWatch with example transit operations data"

    def handle(self, *args, **options):
        Route.objects.all().delete()
        Vehicle.objects.all().delete()
        ServiceAlert.objects.all().delete()
        Incident.objects.all().delete()
        MaintenanceTicket.objects.all().delete()

        routes = [
            Route.objects.create(
                code="M42",
                name="Midtown Loop",
                status="delayed",
                description="Weather-related delays around Midtown corridor.",
            ),
            Route.objects.create(
                code="Q12",
                name="Queens Connector",
                status="normal",
                description="Standard patrol service across the central corridor.",
            ),
            Route.objects.create(
                code="B7",
                name="Harbor Express",
                status="maintenance",
                description="Scheduled maintenance affecting service windows.",
            ),
        ]

        vehicles = [
            Vehicle.objects.create(
                vehicle_id="BUS-101",
                route=routes[0],
                status="maintenance",
                capacity=40,
            ),
            Vehicle.objects.create(
                vehicle_id="BUS-204",
                route=routes[1],
                status="in_service",
                capacity=42,
            ),
            Vehicle.objects.create(
                vehicle_id="BUS-318",
                route=routes[2],
                status="out_of_service",
                capacity=35,
            ),
        ]

        ServiceAlert.objects.create(
            route=routes[0],
            title="Weather delay",
            description="Heavy rain is delaying trips on the Midtown Loop for the next hour.",
            severity="high",
            is_active=True,
        )
        ServiceAlert.objects.create(
            route=routes[2],
            title="Track inspection",
            description="Scheduled inspection is reducing service on Harbor Express.",
            severity="medium",
            is_active=True,
        )
        ServiceAlert.objects.create(
            route=routes[1],
            title="Signal reset",
            description="Brief signal reset is expected near Queens Connector terminals.",
            severity="low",
            is_active=False,
        )

        Incident.objects.create(
            route=routes[0],
            vehicle=vehicles[0],
            title="Signal issue",
            description="Signal malfunction near 42nd Street caused temporary stoppages.",
            severity="medium",
            status="open",
        )
        Incident.objects.create(
            route=routes[1],
            vehicle=vehicles[1],
            title="Door malfunction",
            description="A bus door failed to close properly on a morning run.",
            severity="high",
            status="monitoring",
        )

        MaintenanceTicket.objects.create(
            route=routes[0],
            vehicle=vehicles[0],
            title="Brake inspection",
            description="Brake system inspection required before the next dispatch window.",
            status="open",
            priority="high",
            assigned_to="Maintenance Crew A",
        )
        MaintenanceTicket.objects.create(
            route=routes[2],
            vehicle=vehicles[2],
            title="Tire replacement",
            description="Replace worn tires before returning the bus to service.",
            status="pending",
            priority="critical",
            assigned_to="Fleet Ops Team",
        )

        self.stdout.write(
            self.style.SUCCESS("Seeded RouteWatch with realistic example transit data.")
        )
