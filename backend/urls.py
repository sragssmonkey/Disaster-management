from django.urls import path
from . import views

urlpatterns = [
    # existing submit endpoint (preserved)
    path("reports", views.submit_report, name="submit_report"),

    # new: list reports for frontend
    path("reports/list", views.list_reports, name="list_reports"),

    # Bhuvan proxy endpoint
    path("proxy/bhuvan/", views.bhuvan_proxy, name="bhuvan_proxy"),

    # ML heatmap PNG
    path("ml/heatmap.png", views.ml_heatmap_png, name="ml_heatmap"),
    
    # Emergency Reporting Endpoints (SMS, IVR, USSD)
    path("emergency/sms/", views.sms_emergency_report, name="sms_emergency_report"),
    path("emergency/ivr/", views.ivr_emergency_report, name="ivr_emergency_report"),
    path("emergency/ussd/", views.ussd_emergency_report, name="ussd_emergency_report"),
    path("emergency/reports/", views.list_emergency_reports, name="list_emergency_reports"),
    path("emergency/reports/<str:report_id>/", views.get_emergency_report_details, name="get_emergency_report_details"),
    path("emergency/reports/<str:report_id>/acknowledge/", views.acknowledge_emergency_report, name="acknowledge_emergency_report"),
    path("emergency/reports/<str:report_id>/status/", views.update_emergency_report_status, name="update_emergency_report_status"),
    
    # Webhook Endpoints
    path("webhooks/sms/", views.sms_webhook, name="sms_webhook"),
    path("webhooks/ivr/", views.ivr_webhook, name="ivr_webhook"),
    path("webhooks/ussd/", views.ussd_webhook, name="ussd_webhook"),
    
    # TwiML Endpoints for IVR
    path("ivr/twiml/<str:action>/", views.ivr_twiml, name="ivr_twiml"),
]
