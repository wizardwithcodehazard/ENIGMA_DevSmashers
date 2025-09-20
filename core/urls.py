from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='user-dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard_view, name='doctor-dashboard'),
]

