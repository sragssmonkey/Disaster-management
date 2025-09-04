from django.shortcuts import render

# Create your views here.
import os
import pickle
from django.conf import settings
from django.shortcuts import render

# Path to trained model
model_path = os.path.join(settings.BASE_DIR, "mlmodel/ml_models/earthquake_risk_model.pkl")

# Load once when server starts
with open(model_path, "rb") as f:
    model = pickle.load(f)

from django.shortcuts import render

def earthquake_map(request):
    return render(request, 'mlmodel/earthquake_map.html')

