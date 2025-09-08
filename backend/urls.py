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
]
