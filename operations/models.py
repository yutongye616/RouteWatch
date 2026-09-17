from django.conf import settings
from django.db import models


class Route(models.Model):
    STATUS_CHOICES = [
        ("normal", "Normal"),
        ("delayed", "Delayed"),
        ("suspended", "Suspended"),
        ("maintenance", "Maintenance"),
    ]

    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="normal")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"


class Vehicle(models.Model):
    STATUS_CHOICES = [
        ("in_service", "In Service"),
        ("maintenance", "Maintenance"),
        ("out_of_service", "Out of Service"),
        ("standby", "Standby"),
    ]

    vehicle_id = models.CharField(max_length=30, unique=True)
    route = models.ForeignKey(
        Route,
        on_delete=models.SET_NULL,
        related_name="vehicles",
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="in_service")
    capacity = models.PositiveIntegerField(default=0)
    last_inspection = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["vehicle_id"]

    def __str__(self):
        return self.vehicle_id


class ServiceAlert(models.Model):
    SEVERITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]

    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="alerts")
    title = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default="medium")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.route.code}: {self.title}"


class Incident(models.Model):
    SEVERITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]
    STATUS_CHOICES = [
        ("open", "Open"),
        ("monitoring", "Monitoring"),
        ("resolved", "Resolved"),
    ]

    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="incidents")
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        related_name="incidents",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default="medium")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reported_incidents",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.route.code}: {self.title}"


class MaintenanceTicket(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("pending", "Pending"),
        ("resolved", "Resolved"),
    ]
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]

    route = models.ForeignKey(
        Route,
        on_delete=models.SET_NULL,
        related_name="maintenance_tickets",
        null=True,
        blank=True,
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        related_name="maintenance_tickets",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="medium")
    assigned_to = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
