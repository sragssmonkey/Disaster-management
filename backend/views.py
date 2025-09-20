import os
import requests
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CrowdReport
from rest_framework import generics
from .models import CrowdReport, EmergencyReport, EmergencyResponse
from .serializers import CrowdReportSerializer, EmergencyReportSerializer, EmergencyResponseSerializer
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

    rescuer_count = 0
    rescuer_location = None
    is_rescuer = False

    if request.user.is_authenticated:
        # check if user has the method
        is_rescuer = hasattr(request.user, "is_rescuer") and request.user.is_rescuer()
        rescuer_count = User.objects.filter(role="rescuer").count()

        if is_rescuer:
            try:
                rescuer_location = RescuerLocation.objects.get(user=request.user)
            except RescuerLocation.DoesNotExist:
                rescuer_location = None

    context = {
        "reports": reports,
        "is_rescuer": is_rescuer,
        "active_rescuers": rescuer_count,
        "rescuer_location": rescuer_location,
    }
    return render(request, "frontend/view_report.html", context)


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

# -------------------------
# Emergency Reporting Views (SMS, IVR, USSD)
# -------------------------

import re
import uuid
from django.utils import timezone
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def sms_emergency_report(request):
    """
    Handle emergency reports via SMS
    Expected SMS format: "EMERGENCY <category> <severity> <description> <location>"
    Example: "EMERGENCY flood 3 water level rising fast near main road"
    """
    try:
        from .sms_service import SMSService
        from .location_service import LocationService
        
        data = request.data
        phone_number = data.get('phone_number', '').strip()
        message = data.get('message', '').strip()
        
        if not phone_number or not message:
            return JsonResponse({
                'status': 'error',
                'message': 'Phone number and message are required'
            }, status=400)
        
        # Parse SMS message using SMS service
        sms_service = SMSService()
        parsed_data = sms_service.parse_emergency_sms(message)
        
        if not parsed_data['valid']:
            # Send error message back to user
            sms_service.send_sms(phone_number, parsed_data['error'])
            return JsonResponse({
                'status': 'error',
                'message': parsed_data['error']
            }, status=400)
        
        # Detect location from phone number
        location_info = LocationService.detect_location_from_phone_number(phone_number)
        
        # Create emergency report
        with transaction.atomic():
            emergency_report = EmergencyReport.objects.create(
                channel='sms',
                phone_number=phone_number,
                category=parsed_data['category'],
                severity=parsed_data['severity'],
                description=parsed_data['description'],
                district=location_info.get('district') if location_info else None,
                state=location_info.get('state') if location_info else None,
                raw_data={
                    'original_message': message,
                    'parsed_data': parsed_data
                }
            )
            
            # Calculate priority score
            emergency_report.priority_score = emergency_report.get_priority_score()
            emergency_report.save()
        
        # Send confirmation SMS
        sms_service.send_emergency_confirmation(phone_number, emergency_report.report_id)
        
        return JsonResponse({
            'status': 'success',
            'report_id': emergency_report.report_id,
            'message': f'Emergency report {emergency_report.report_id} received. Help is on the way.'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Failed to process SMS report: {str(e)}'
        }, status=500)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def ivr_emergency_report(request):
    """
    Handle emergency reports via IVR (Interactive Voice Response)
    """
    try:
        from .ivr_service import IVRService
        from .location_service import LocationService
        
        data = request.data
        phone_number = data.get('phone_number', '').strip()
        call_id = data.get('call_id', '')
        transcript = data.get('transcript', '').strip()
        category = data.get('category', 'other')
        severity = int(data.get('severity', 1))
        location = data.get('location', '')
        
        if not phone_number:
            return JsonResponse({
                'status': 'error',
                'message': 'Phone number is required'
            }, status=400)
        
        # Detect location from phone number if not provided
        location_info = None
        if not location:
            location_info = LocationService.detect_location_from_phone_number(phone_number)
        
        # Create emergency report
        with transaction.atomic():
            emergency_report = EmergencyReport.objects.create(
                channel='ivr',
                phone_number=phone_number,
                category=category,
                severity=severity,
                description=transcript or 'Emergency reported via voice call',
                address=location or (LocationService.format_location_for_report(location_info) if location_info else ''),
                district=location_info.get('district') if location_info else None,
                state=location_info.get('state') if location_info else None,
                raw_data={
                    'call_id': call_id,
                    'transcript': transcript,
                    'category': category,
                    'severity': severity,
                    'location': location
                }
            )
            
            # Calculate priority score
            emergency_report.priority_score = emergency_report.get_priority_score()
            emergency_report.save()
        
        # Send confirmation call
        ivr_service = IVRService()
        ivr_service.send_ivr_confirmation(phone_number, emergency_report.report_id)
        
        return JsonResponse({
            'status': 'success',
            'report_id': emergency_report.report_id,
            'message': f'Emergency report {emergency_report.report_id} received. Help is on the way.'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Failed to process IVR report: {str(e)}'
        }, status=500)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def ussd_emergency_report(request):
    """
    Handle emergency reports via USSD
    """
    try:
        from .ussd_service import USSDService
        from .location_service import LocationService
        
        data = request.data
        phone_number = data.get('phone_number', '').strip()
        session_id = data.get('session_id', '')
        menu_level = data.get('menu_level', 1)
        selected_option = data.get('selected_option', '')
        user_input = data.get('user_input', '')
        session_data = data.get('session_data', {})
        
        if not phone_number:
            return JsonResponse({
                'status': 'error',
                'message': 'Phone number is required'
            }, status=400)
        
        # Process USSD request using USSD service
        ussd_service = USSDService()
        result = ussd_service.process_ussd_request(
            phone_number, session_id, menu_level, user_input, session_data
        )
        
        # If it's a successful report creation, add location detection
        if result.get('status') == 'success' and 'report_id' in result:
            try:
                # Detect location from phone number
                location_info = LocationService.detect_location_from_phone_number(phone_number)
                
                # Update the emergency report with location info
                emergency_report = EmergencyReport.objects.get(report_id=result['report_id'])
                if location_info:
                    emergency_report.district = location_info.get('district')
                    emergency_report.state = location_info.get('state')
                    emergency_report.save()
            except Exception as e:
                logger.error(f"Failed to update location for USSD report: {str(e)}")
        
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Failed to process USSD report: {str(e)}'
        }, status=500)


@api_view(['GET'])
def list_emergency_reports(request):
    """
    List all emergency reports with filtering options
    """
    try:
        queryset = EmergencyReport.objects.all()
        
        # Apply filters
        status_filter = request.GET.get('status')
        category_filter = request.GET.get('category')
        severity_filter = request.GET.get('severity')
        channel_filter = request.GET.get('channel')
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if category_filter:
            queryset = queryset.filter(category=category_filter)
        if severity_filter:
            queryset = queryset.filter(severity=int(severity_filter))
        if channel_filter:
            queryset = queryset.filter(channel=channel_filter)
        
        # Order by priority and creation time
        queryset = queryset.order_by('-priority_score', '-created_at')
        
        serializer = EmergencyReportSerializer(queryset, many=True)
        return Response({
            'status': 'success',
            'reports': serializer.data,
            'count': queryset.count()
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Failed to fetch emergency reports: {str(e)}'
        }, status=500)


@api_view(['POST'])
def acknowledge_emergency_report(request, report_id):
    """
    Acknowledge an emergency report
    """
    try:
        if not request.user.is_authenticated:
            return Response({
                'status': 'error',
                'message': 'Authentication required'
            }, status=401)
        
        try:
            emergency_report = EmergencyReport.objects.get(report_id=report_id)
        except EmergencyReport.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Emergency report not found'
            }, status=404)
        
        # Update report status
        emergency_report.status = 'acknowledged'
        emergency_report.acknowledged_at = timezone.now()
        emergency_report.assigned_to = request.user
        emergency_report.save()
        
        # Create response record
        EmergencyResponse.objects.create(
            emergency_report=emergency_report,
            responder=request.user,
            response_type='acknowledgment',
            message=f'Emergency report {report_id} acknowledged by {request.user.username}'
        )
        
        return Response({
            'status': 'success',
            'message': f'Emergency report {report_id} acknowledged'
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Failed to acknowledge emergency report: {str(e)}'
        }, status=500)


@api_view(['POST'])
def update_emergency_report_status(request, report_id):
    """
    Update the status of an emergency report
    """
    try:
        if not request.user.is_authenticated:
            return Response({
                'status': 'error',
                'message': 'Authentication required'
            }, status=401)
        
        try:
            emergency_report = EmergencyReport.objects.get(report_id=report_id)
        except EmergencyReport.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Emergency report not found'
            }, status=404)
        
        new_status = request.data.get('status')
        message = request.data.get('message', '')
        
        if new_status not in [choice[0] for choice in EmergencyReport.STATUS_CHOICES]:
            return Response({
                'status': 'error',
                'message': 'Invalid status'
            }, status=400)
        
        # Update report status
        emergency_report.status = new_status
        if new_status == 'resolved':
            emergency_report.resolved_at = timezone.now()
        emergency_report.save()
        
        # Create response record
        EmergencyResponse.objects.create(
            emergency_report=emergency_report,
            responder=request.user,
            response_type='update',
            message=message or f'Status updated to {new_status} by {request.user.username}'
        )
        
        return Response({
            'status': 'success',
            'message': f'Emergency report {report_id} status updated to {new_status}'
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Failed to update emergency report status: {str(e)}'
        }, status=500)


@api_view(['GET'])
def get_emergency_report_details(request, report_id):
    """
    Get detailed information about a specific emergency report
    """
    try:
        try:
            emergency_report = EmergencyReport.objects.get(report_id=report_id)
        except EmergencyReport.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Emergency report not found'
            }, status=404)
        
        serializer = EmergencyReportSerializer(emergency_report)
        responses = EmergencyResponse.objects.filter(emergency_report=emergency_report).order_by('-created_at')
        response_serializer = EmergencyResponseSerializer(responses, many=True)
        
        return Response({
            'status': 'success',
            'report': serializer.data,
            'responses': response_serializer.data
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': f'Failed to fetch emergency report details: {str(e)}'
        }, status=500)


# -------------------------
# Webhook Handlers for SMS, IVR, USSD
# -------------------------

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def sms_webhook(request):
    """
    Handle incoming SMS webhooks from SMS gateway
    """
    try:
        from .sms_service import SMSWebhookHandler
        
        # Extract SMS data from webhook
        phone_number = request.data.get('From', '')
        message = request.data.get('Body', '')
        
        if not phone_number or not message:
            return JsonResponse({
                'status': 'error',
                'message': 'Missing phone number or message'
            }, status=400)
        
        # Handle incoming SMS
        result = SMSWebhookHandler.handle_incoming_sms(request.data)
        
        if result['status'] == 'success':
            # Create emergency report
            from .models import EmergencyReport
            from .location_service import LocationService
            
            parsed_data = result['parsed_data']
            location_info = LocationService.detect_location_from_phone_number(phone_number)
            
            emergency_report = EmergencyReport.objects.create(
                channel='sms',
                phone_number=phone_number,
                category=parsed_data['category'],
                severity=parsed_data['severity'],
                description=parsed_data['description'],
                district=location_info.get('district') if location_info else None,
                state=location_info.get('state') if location_info else None,
                raw_data={
                    'webhook_data': request.data,
                    'parsed_data': parsed_data
                }
            )
            
            # Calculate priority score
            emergency_report.priority_score = emergency_report.get_priority_score()
            emergency_report.save()
            
            # Send confirmation SMS
            from .sms_service import SMSService
            sms_service = SMSService()
            sms_service.send_emergency_confirmation(phone_number, emergency_report.report_id)
        
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'SMS webhook handling failed: {str(e)}'
        }, status=500)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def ivr_webhook(request):
    """
    Handle incoming IVR webhooks from Twilio
    """
    try:
        from .ivr_service import IVRWebhookHandler, IVRService
        
        webhook_type = request.data.get('webhook_type', 'call_status')
        
        if webhook_type == 'call_status':
            result = IVRWebhookHandler.handle_call_status(request.data)
        elif webhook_type == 'recording_complete':
            result = IVRWebhookHandler.handle_recording_complete(request.data)
        else:
            result = {
                'status': 'error',
                'message': 'Unknown webhook type'
            }
        
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'IVR webhook handling failed: {str(e)}'
        }, status=500)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def ussd_webhook(request):
    """
    Handle incoming USSD webhooks
    """
    try:
        from .ussd_service import USSDWebhookHandler
        
        webhook_type = request.data.get('webhook_type', 'ussd_request')
        
        if webhook_type == 'ussd_request':
            result = USSDWebhookHandler.handle_ussd_request(request.data)
        elif webhook_type == 'session_end':
            result = USSDWebhookHandler.handle_ussd_session_end(request.data)
        else:
            result = {
                'status': 'error',
                'message': 'Unknown webhook type'
            }
        
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'USSD webhook handling failed: {str(e)}'
        }, status=500)


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def ivr_twiml(request, action=None):
    """
    Generate TwiML responses for Twilio IVR
    """
    try:
        from .ivr_service import IVRService
        
        ivr_service = IVRService()
        
        if action == 'welcome':
            twiml = ivr_service.generate_twiml_response('welcome')
        elif action == 'category':
            twiml = ivr_service.generate_twiml_response('category_selection')
        elif action == 'severity':
            twiml = ivr_service.generate_twiml_response('severity_selection')
        elif action == 'description':
            twiml = ivr_service.generate_twiml_response('description_prompt')
        elif action == 'location':
            twiml = ivr_service.generate_twiml_response('location_prompt')
        elif action == 'confirmation':
            report_id = request.GET.get('report_id', '')
            twiml = ivr_service.generate_twiml_response('confirmation', report_id=report_id)
        else:
            twiml = ivr_service.generate_twiml_response('error', message='Invalid action')
        
        from django.http import HttpResponse
        return HttpResponse(twiml, content_type='text/xml')
        
    except Exception as e:
        from django.http import HttpResponse
        error_twiml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice" language="en-IN">An error occurred. Please try again later.</Say>
</Response>'''
        return HttpResponse(error_twiml, content_type='text/xml')
