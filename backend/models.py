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


class EmergencyReport(models.Model):
    """Model for emergency reports from SMS, IVR, and USSD channels"""
    
    CHANNEL_CHOICES = [
        ("sms", "SMS"),
        ("ivr", "IVR (Voice Call)"),
        ("ussd", "USSD"),
        ("web", "Web Interface"),
    ]
    
    LANGUAGE_CHOICES = [
        ("en", "English"),
        ("hi", "Hindi"),
        ("bn", "Bengali"),
        ("te", "Telugu"),
        ("mr", "Marathi"),
        ("ta", "Tamil"),
        ("gu", "Gujarati"),
        ("kn", "Kannada"),
        ("ml", "Malayalam"),
        ("pa", "Punjabi"),
        ("or", "Odia"),
        ("as", "Assamese"),
    ]
    
    CATEGORY_CHOICES = [
        ("flood", "Flood"),
        ("landslide", "Landslide"),
        ("roadblock", "Roadblock"),
        ("medical", "Medical Emergency"),
        ("fire", "Fire"),
        ("earthquake", "Earthquake"),
        ("cyclone", "Cyclone"),
        ("other", "Other"),
    ]
    
    SEVERITY_CHOICES = [
        (1, "Low"),
        (2, "Medium"),
        (3, "High"),
        (4, "Critical"),
    ]
    
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("acknowledged", "Acknowledged"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("false_alarm", "False Alarm"),
    ]

    # Report identification
    report_id = models.CharField(max_length=50, unique=True, blank=True)
    channel = models.CharField(max_length=10, choices=CHANNEL_CHOICES)
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default="en")
    
    # Contact information
    phone_number = models.CharField(max_length=15)
    caller_name = models.CharField(max_length=100, blank=True, null=True)
    
    # Emergency details
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    severity = models.IntegerField(choices=SEVERITY_CHOICES, default=1)
    description = models.TextField()
    
    # Location information
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    
    # Processing information
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                   null=True, blank=True, related_name="assigned_emergencies")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # Additional data
    raw_data = models.JSONField(default=dict, blank=True)  # Store original SMS/IVR data
    follow_up_required = models.BooleanField(default=False)
    priority_score = models.FloatField(default=0.0)  # Calculated priority based on various factors
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['category', 'severity']),
            models.Index(fields=['phone_number']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.report_id:
            import uuid
            self.report_id = f"EMR-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Emergency Report {self.report_id} - {self.category} ({self.get_severity_display()})"
    
    def get_priority_score(self):
        """Calculate priority score based on severity, category, and other factors"""
        base_score = self.severity * 25
        
        # Category multipliers
        category_multipliers = {
            'medical': 1.5,
            'fire': 1.4,
            'earthquake': 1.3,
            'flood': 1.2,
            'cyclone': 1.2,
            'landslide': 1.1,
            'roadblock': 1.0,
            'other': 0.9,
        }
        
        multiplier = category_multipliers.get(self.category, 1.0)
        return base_score * multiplier


class EmergencyResponse(models.Model):
    """Model to track responses to emergency reports"""
    
    emergency_report = models.ForeignKey(EmergencyReport, on_delete=models.CASCADE, related_name="responses")
    responder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    response_type = models.CharField(max_length=20, choices=[
        ("acknowledgment", "Acknowledgment"),
        ("update", "Status Update"),
        ("resolution", "Resolution"),
        ("escalation", "Escalation"),
    ])
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Response to {self.emergency_report.report_id} by {self.responder.username}"
