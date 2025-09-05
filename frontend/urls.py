from django.urls import path
from django.contrib.auth import views as auth_views
from frontend import views as frontend_views
from backend import views as backend_views

urlpatterns = [
    # Auth
    path('signup/', frontend_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='frontend/login.html'), name='login'),
    path('logout/', frontend_views.logout_view, name='logout'),

    # Frontend pages
    path("", frontend_views.home, name="home"),
    path("report/", frontend_views.report, name="report"),
    path("view_report/", frontend_views.view_report, name="view_report"),
    path("globe/", frontend_views.globe, name="globe"),

    # APIs
    path("api/reports/", backend_views.CrowdReportList.as_view(), name="api-reports"),
    path("api/reports/simple/", frontend_views.reports_api, name="reports_api"),  # avoid conflict
    path("api/update_rescuer_location/", backend_views.update_rescuer_location, name="update_rescuer_location"),
    path("api/get_rescuers/", backend_views.get_rescuers, name="get_rescuers"),
]
