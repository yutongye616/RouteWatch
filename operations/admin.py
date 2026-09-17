from django.contrib import admin

from .models import Incident, MaintenanceTicket, Route, ServiceAlert, Vehicle


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "status")
    list_filter = ("status",)
    search_fields = ("code", "name")


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("vehicle_id", "route", "status")
    list_filter = ("status", "route")
    search_fields = ("vehicle_id",)


@admin.register(ServiceAlert)
class ServiceAlertAdmin(admin.ModelAdmin):
    list_display = ("route", "title", "severity", "is_active", "created_at")
    list_filter = ("severity", "is_active")


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ("route", "title", "severity", "status", "created_at")
    list_filter = ("status", "severity")


@admin.register(MaintenanceTicket)
class MaintenanceTicketAdmin(admin.ModelAdmin):
    list_display = ("title", "route", "status", "priority", "assigned_to")
    list_filter = ("status", "priority")
