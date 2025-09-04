from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CrowdReport

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
