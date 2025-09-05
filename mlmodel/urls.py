from django.urls import path
from . import views

urlpatterns = [
    path("disaster_map/", views.disaster_map, name="disaster_map"),
]

