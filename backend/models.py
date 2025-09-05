from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class RescuerLocation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lat = models.FloatField()
    lng = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} @ ({self.lat}, {self.lng})"



class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("normal", "Normal User"),
        ("rescuer", "Rescuer"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="normal")

    def is_rescuer(self):
        return self.role == "rescuer"


class CrowdReport(models.Model):
    CATEGORY_CHOICES = [
        ("flood", "Flood"),
        ("landslide", "Landslide"),
        ("roadblock", "Roadblock"),
        ("medical", "Medical"),
        ("other", "Other"),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="other")
    severity = models.IntegerField(default=0)
    note = models.TextField(blank=True, null=True)
    lat = models.FloatField()
    lng = models.FloatField()
    photo = models.ImageField(upload_to="reports/", blank=True, null=True)
    device_fingerprint = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} @ ({self.lat}, {self.lng})"
