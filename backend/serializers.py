from rest_framework import serializers
from django.conf import settings
from .models import CrowdReport, EmergencyReport, EmergencyResponse

class CrowdReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrowdReport
        fields = "__all__"
        read_only_fields = ("created_at",)

    def validate_category(self, value):
        allowed = [c[0] for c in CrowdReport.CATEGORY_CHOICES]  # 👈 fixed
        if value not in allowed:
            raise serializers.ValidationError("Invalid category")
        return value

    def validate_photo(self, value):
        if not value:
            return value
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Image too large (max 5 MB)")
        return value

    def validate(self, data):
        bounds = settings.INDIA_BOUNDS
        lat, lng = float(data["lat"]), float(data["lng"])
        if not (bounds["MIN_LAT"] <= lat <= bounds["MAX_LAT"] and bounds["MIN_LNG"] <= lng <= bounds["MAX_LNG"]):
            raise serializers.ValidationError({"lat": "Outside India bounds", "lng": "Outside India bounds"})
        return data

class EmergencyReportSerializer(serializers.ModelSerializer):
    priority_score = serializers.ReadOnlyField()
    report_id = serializers.ReadOnlyField()
    
    class Meta:
        model = EmergencyReport
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "acknowledged_at", "resolved_at")
    
    def validate_phone_number(self, value):
        # Basic phone number validation
        import re
        if not re.match(r'^\+?[1-9]\d{1,14}$', value):
            raise serializers.ValidationError("Invalid phone number format")
        return value
    
    def validate_severity(self, value):
        if value not in [1, 2, 3, 4]:
            raise serializers.ValidationError("Severity must be between 1 and 4")
        return value


class EmergencyResponseSerializer(serializers.ModelSerializer):
    responder_name = serializers.CharField(source='responder.username', read_only=True)
    
    class Meta:
        model = EmergencyResponse
        fields = "__all__"
        read_only_fields = ("created_at",)


class CycloneInputSerializer(serializers.Serializer):
    num_points = serializers.IntegerField(required=False, default=15)

