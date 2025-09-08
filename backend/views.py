import os
import requests
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
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
Bhuvan_base = "https://bhuvan-vec2.nrsc.gov.in/bhuvan"
BHUVAN_TOKEN = os.getenv("BHUVAN_TOKEN", "").strip()

@csrf_exempt
@require_GET
def bhuvan_proxy(request):
    path = request.GET.get("path", "wms")

    qs_items = []
    for k, v in request.GET.items():
        if k == "path":
            continue
        qs_items.append(f"{k}={requests.utils.quote(v, safe='/:?&=,+%')}")
    qs = "&".join(qs_items)

    target = f"{Bhuvan_base}/{path}"
    if qs:
        target = f"{target}?{qs}"

    if BHUVAN_TOKEN and "token=" not in target:
        sep = "&" if "?" in target else "?"
        target = f"{target}{sep}token={BHUVAN_TOKEN}"

    try:
        resp = requests.get(target, stream=True, timeout=20)
    except requests.RequestException as e:
        return JsonResponse({"error": "failed to contact bhuvan", "detail": str(e)}, status=502)

    content_type = resp.headers.get("Content-Type", "application/octet-stream")
    django_resp = StreamingHttpResponse(resp.raw, status=resp.status_code, content_type=content_type)

    if "content-disposition" in resp.headers:
        django_resp["Content-Disposition"] = resp.headers["content-disposition"]

    django_resp["Access-Control-Allow-Origin"] = "*"
    django_resp["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    django_resp["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

    return django_resp








# --- Begin appended Bhuvan + reports + ML heatmap views ---

import os
import io
from django.http import StreamingHttpResponse, JsonResponse, HttpResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt

# existing models import assumptions (CrowdReport likely already imported elsewhere)
try:
    from .models import CrowdReport
except Exception:
    CrowdReport = None

# -------------------------
# Bhuvan proxy (lazy import)
# -------------------------
Bhuvan_base = "https://bhuvan-vec2.nrsc.gov.in/bhuvan"
BHUVAN_TOKEN = os.getenv("BHUVAN_TOKEN", "").strip()

@csrf_exempt
@require_GET
def bhuvan_proxy(request):
    """
    Proxy GET requests to Bhuvan to avoid client-side CORS.
    Usage example:
      /proxy/bhuvan/?path=wms&SERVICE=WMS&REQUEST=GetCapabilities
      /proxy/bhuvan/?path=wms&SERVICE=WMS&REQUEST=GetMap&LAYERS=...
    If 'path' is omitted it defaults to 'wms'.
    """
    # Lazy import so server can start even if requests not installed
    try:
        import requests
    except ModuleNotFoundError:
        return JsonResponse({"error": "requests library not installed. Run pip install requests"}, status=500)

    path = request.GET.get("path", "wms")

    # rebuild querystring without 'path'
    qs_items = []
    for k, v in request.GET.items():
        if k == "path":
            continue
        qs_items.append(f"{k}={requests.utils.quote(v, safe='/:?&=,+%')}")
    qs = "&".join(qs_items)

    target = f"{Bhuvan_base}/{path}"
    if qs:
        target = f"{target}?{qs}"

    # Append token server-side if configured
    if BHUVAN_TOKEN and "token=" not in target:
        sep = "&" if "?" in target else "?"
        target = f"{target}{sep}token={BHUVAN_TOKEN}"

    try:
        resp = requests.get(target, stream=True, timeout=20)
    except requests.RequestException as e:
        return JsonResponse({"error": "failed to contact bhuvan", "detail": str(e)}, status=502)

    content_type = resp.headers.get("Content-Type", "application/octet-stream")
    django_resp = StreamingHttpResponse(resp.raw, status=resp.status_code, content_type=content_type)

    if "content-disposition" in resp.headers:
        django_resp["Content-Disposition"] = resp.headers["content-disposition"]

    # allow cross origin for safety (server → server)
    django_resp["Access-Control-Allow-Origin"] = "*"
    django_resp["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    django_resp["Access-Control-Allow-Headers"] = "Content-Type, Authorization"

    return django_resp


# -------------------------
# Reports listing endpoint
# -------------------------
@require_GET
def list_reports(request):
    """
    Return recent CrowdReport objects as JSON for frontend mapping.
    Endpoint: /reports/list
    """
    if CrowdReport is None:
        return JsonResponse({"error": "CrowdReport model not available"}, status=500)
    try:
        qs = CrowdReport.objects.order_by("-id")[:1000]  # keep reasonable limit
    except Exception:
        # fallback: try without order
        qs = CrowdReport.objects.all()[:1000]
    out = []
    for r in qs:
        # guard for missing attributes
        cid = getattr(r, "id", None)
        lat = getattr(r, "lat", None)
        lng = getattr(r, "lng", None)
        category = getattr(r, "category", "")
        severity = getattr(r, "severity", None)
        note = getattr(r, "note", "") or ""
        created = getattr(r, "created_at", None)
        created_iso = created.isoformat() if created is not None else None
        try:
            lat_f = float(lat)
            lng_f = float(lng)
        except Exception:
            # skip invalid coordinates
            continue
        out.append({
            "id": cid,
            "lat": lat_f,
            "lng": lng_f,
            "category": category,
            "severity": severity,
            "note": note,
            "created_at": created_iso,
        })
    return JsonResponse({"reports": out})


# ------------------------- GPT
# ML heatmap PNG generator
# -------------------------
def ml_heatmap_png(request):
    """
    Return a generated PNG heatmap. This example uses numpy + matplotlib.
    If those libs are not installed, returns a JSON error asking to install.
    URL: /ml/heatmap.png
    """
    # lazy imports
    try:
        import numpy as np
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:
        return JsonResponse({"error": "required libraries missing for heatmap", "detail": str(e)}, status=500)

    # Replace this with your actual ML output -> 2D array with shape (H, W)
    # Here we create a small example heatmap; replace `data` with your model output.
    data = np.random.random((512, 512))

    fig = plt.figure(frameon=False)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.imshow(data, cmap='hot', origin='lower', interpolation='nearest')
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    return HttpResponse(buf.read(), content_type='image/png')

# --- End appended views ---
