from django.urls import path
from . import views

urlpatterns = [
    path("reports", views.submit_report, name="submit_report"),  # <-- no slash at start
]
