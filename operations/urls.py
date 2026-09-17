from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("routes/", views.route_list, name="route_list"),
    path("alerts/", views.service_alert_list, name="service_alert_list"),
    path("alerts/new/", views.service_alert_create, name="service_alert_create"),
    path("incidents/", views.incident_list, name="incident_list"),
    path("incidents/new/", views.incident_create, name="incident_create"),
    path("maintenance/", views.maintenance_ticket_list, name="maintenance_ticket_list"),
    path("maintenance/new/", views.maintenance_ticket_create, name="maintenance_ticket_create"),
]
