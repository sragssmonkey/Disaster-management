from django.urls import path
from django.contrib.auth import views as auth_views
from frontend import views as frontend_views


urlpatterns = [
    # frontend views
    path('signup/', frontend_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='frontend/login.html'), name='login'),
    path('logout/', frontend_views.logout_view, name='logout'),
    path("", frontend_views.home, name="home"),
    path('report/',frontend_views.report,name="report"),
    path('view_report/',frontend_views.view_report,name="view_report"),
   

    path("report/", frontend_views.report, name="report"),
    path("view_report/", frontend_views.view_report, name="view_report"),
    path("api/reports/", frontend_views.reports_api, name="reports_api"),  # NEW




    # backend views
    path("globe/",frontend_views.globe, name="globe"),
    
]
