from django.urls import path
from . import views

urlpatterns = [
    path('earthquake-map/', views.earthquake_map, name='earthquake_map'),
]
