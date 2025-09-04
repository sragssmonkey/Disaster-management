from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm


def logout_view(request):
    logout(request)
    return redirect('home')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Django's login()
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'frontend/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "frontend/login.html", {"form": form})


def home(request):
    return render(request, "frontend/home.html")


def globe(request):
    return render(request, "frontend/globe.html")

def report(request):
    return render(request,"frontend/report.html")

def view_report(request):
    return render(request,"frontend/view_report.html")

import json
from django.shortcuts import render

from django.shortcuts import render
import json

def globe_view(request):
    # Example: Your ML model output
    predictions = [
        {"lat": 28.6139, "lon": 77.2090, "risk": 0.9},   # Delhi
        {"lat": 19.0760, "lon": 72.8777, "risk": 0.7},   # Mumbai
        {"lat": 13.0827, "lon": 80.2707, "risk": 0.4},   # Chennai
        {"lat": 22.5726, "lon": 88.3639, "risk": 0.6},   # Kolkata
    ]

    context = {
        "predictions": json.dumps(predictions)  # send to frontend as JSON
    }
    return render(request, "frontend/globe.html", context)

from django.http import JsonResponse
from backend.models import CrowdReport

def reports_api(request):
    data = list(CrowdReport.objects.values(
        "id",
        "category",
        "severity",
        "note",
        "lat",
        "lng",
        "created_at"
    ).order_by("-created_at"))  # newest first
    return JsonResponse(data, safe=False)
