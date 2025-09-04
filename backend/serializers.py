from rest_framework import serializers
from django.conf import settings
from .models import Report, CATEGORY_CHOICES

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"
        read_only_fields = ("created_at",)

    def validate_category(self, value):
        allowed = [c[0] for c in CATEGORY_CHOICES]
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
