import json
import urllib.request

from django.shortcuts import redirect, render

from .models import Incident, MaintenanceTicket, Route, ServiceAlert, Vehicle


def fetch_nyc_incidents(limit=5):
    url = (
        "https://data.cityofnewyork.us/resource/qiz3-axqb.json"
        f"?$limit={limit}&$order=crash_date%20DESC"
    )

    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception:
        return [{
            "title": "Public road data unavailable",
            "location": "NYC roadway",
            "injuries": "N/A",
            "factor": "Public road data unavailable",
            "status": "monitoring",
            "severity": "medium",
        }]

    if not payload:
        return [{
            "title": "Public road data unavailable",
            "location": "NYC roadway",
            "injuries": "N/A",
            "factor": "Public road data unavailable",
            "status": "monitoring",
            "severity": "medium",
        }]

    incidents = []
    for item in payload:
        injuries = item.get("number_of_persons_injured") or "0"
        location = (
            item.get("on_street_name")
            or item.get("cross_street_name")
            or item.get("location_address")
            or "NYC roadway"
        )
        factor = item.get("contributing_factor_vehicle_1") or "Unspecified"
        incidents.append({
            "title": item.get("borough") or "NYC roadway",
            "location": location,
            "injuries": injuries,
            "factor": factor,
            "status": "open" if injuries not in ("0", 0) else "monitoring",
            "severity": "critical" if injuries not in ("0", 0) else "medium",
        })
    return incidents


def get_nyc_road_summary():
    incidents = fetch_nyc_incidents(limit=1)
    item = incidents[0]
    return {
        "location": item.get("location", "NYC roadway"),
        "injuries": item.get("injuries", "N/A"),
        "factor": item.get("factor", "Public road data unavailable"),
    }


def home(request):
    routes = fetch_nyc_incidents(limit=5)
    total_routes = len(routes)
    active_alerts = sum(1 for item in routes if str(item.get("injuries", "0")).strip() not in ("0", "N/A"))
    open_incidents = len(routes)
    open_maintenance = 0

    context = {
        "total_routes": total_routes,
        "active_alerts": active_alerts,
        "open_incidents": open_incidents,
        "open_maintenance": open_maintenance,
        "routes": routes,
        "road_data": get_nyc_road_summary(),
    }
    return render(request, "operations/home.html", context)


def route_list(request):
    routes = fetch_nyc_incidents(limit=10)
    return render(request, "operations/route_list.html", {"routes": routes})


def service_alert_list(request):
    alerts = ServiceAlert.objects.select_related("route").all()
    return render(request, "operations/service_alert_list.html", {"alerts": alerts})


def service_alert_create(request):
    if request.method == "POST":
        route_id = request.POST.get("route")
        title = request.POST.get("title")
        description = request.POST.get("description")
        severity = request.POST.get("severity", "medium")
        is_active = request.POST.get("is_active") == "on"

        if route_id and title and description:
            ServiceAlert.objects.create(
                route_id=route_id,
                title=title,
                description=description,
                severity=severity,
                is_active=is_active,
            )
            return redirect("service_alert_list")

    routes = Route.objects.all()
    return render(request, "operations/service_alert_form.html", {"routes": routes})


def incident_list(request):
    incidents = Incident.objects.select_related("route", "vehicle").all()
    return render(request, "operations/incident_list.html", {"incidents": incidents})


def incident_create(request):
    if request.method == "POST":
        route_id = request.POST.get("route")
        vehicle_id = request.POST.get("vehicle")
        title = request.POST.get("title")
        description = request.POST.get("description")
        severity = request.POST.get("severity", "medium")
        status = request.POST.get("status", "open")

        if route_id and title and description:
            Incident.objects.create(
                route_id=route_id,
                vehicle_id=vehicle_id or None,
                title=title,
                description=description,
                severity=severity,
                status=status,
            )
            return redirect("incident_list")

    routes = Route.objects.all()
    vehicles = Vehicle.objects.select_related("route").all()
    return render(
        request,
        "operations/incident_form.html",
        {"routes": routes, "vehicles": vehicles},
    )


def maintenance_ticket_list(request):
    tickets = MaintenanceTicket.objects.select_related("route", "vehicle").all()
    return render(request, "operations/maintenance_ticket_list.html", {"tickets": tickets})


def maintenance_ticket_create(request):
    if request.method == "POST":
        route_id = request.POST.get("route")
        vehicle_id = request.POST.get("vehicle")
        title = request.POST.get("title")
        description = request.POST.get("description")
        status = request.POST.get("status", "open")
        priority = request.POST.get("priority", "medium")
        assigned_to = request.POST.get("assigned_to", "")

        if route_id and title and description:
            MaintenanceTicket.objects.create(
                route_id=route_id,
                vehicle_id=vehicle_id or None,
                title=title,
                description=description,
                status=status,
                priority=priority,
                assigned_to=assigned_to,
            )
            return redirect("maintenance_ticket_list")

    routes = Route.objects.all()
    vehicles = Vehicle.objects.select_related("route").all()
    return render(
        request,
        "operations/maintenance_ticket_form.html",
        {"routes": routes, "vehicles": vehicles},
    )
