from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CrowdReport
from rest_framework import generics
from .models import CrowdReport
from .serializers import CrowdReportSerializer
from django.http import JsonResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import RescuerLocation
import json
from django.contrib.auth import get_user_model
from .models import RescuerLocation
from django.shortcuts import render

User = get_user_model()

def view_report(request):
    reports = CrowdReport.objects.all().order_by("-created_at")

    rescuer_count = User.objects.filter(role="rescuer").count()
    rescuer_location = None

    if request.user.is_authenticated and request.user.is_rescuer():
        try:
            rescuer_location = RescuerLocation.objects.get(user=request.user)
        except RescuerLocation.DoesNotExist:
            rescuer_location = None

    context = {
        "reports": reports,
        "is_rescuer": request.user.is_authenticated and request.user.is_rescuer(),
        "active_rescuers": rescuer_count,
        "rescuer_location": rescuer_location,
    }
    return render(request, "view_report.html", context)


@csrf_exempt
def update_rescuer_location(request):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            lat = data.get("lat")
            lng = data.get("lng")

            if lat is not None and lng is not None:
                RescuerLocation.objects.update_or_create(
                    user=request.user,
                    defaults={"lat": lat, "lng": lng}
                )
                return JsonResponse({"status": "ok"})
            else:
                return JsonResponse({"status": "invalid data"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "unauthorized"}, status=401)


def get_rescuers(request):
    if request.user.is_authenticated:
        rescuers = list(
            RescuerLocation.objects.values("lat", "lng", "updated_at")
        )
        return JsonResponse({"count": len(rescuers), "rescuers": rescuers})
    return JsonResponse({"status": "unauthorized"}, status=401)



class CrowdReportList(generics.ListCreateAPIView):
    queryset = CrowdReport.objects.all().order_by("-created_at")
    serializer_class = CrowdReportSerializer


@csrf_exempt   # remove later if you add CSRF tokens
def submit_report(request):
    if request.method == "POST":
        category = request.POST.get("category", "other")
        severity = request.POST.get("severity", 0)
        note = request.POST.get("note", "")
        lat = request.POST.get("lat")
        lng = request.POST.get("lng")
        photo = request.FILES.get("photo")
        device_fp = request.POST.get("device_fingerprint", "")

        # validation
        if not lat or not lng:
            return JsonResponse({"error": "Latitude and Longitude required"}, status=400)

        report = CrowdReport.objects.create(
            category=category,
            severity=int(severity),
            note=note,
            lat=float(lat),
            lng=float(lng),
            photo=photo,
            device_fingerprint=device_fp,
        )

        return JsonResponse({"status": "ok", "id": report.id})

    return JsonResponse({"error": "Invalid method"}, status=405)
