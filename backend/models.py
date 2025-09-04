from django.db import models

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
