from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='user-dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard_view, name='doctor-dashboard'),
    path('complete-profile/', views.complete_profile_view, name='complete-profile'),
    path('stability-check/', views.stability_view, name='stability-check'),
    path('predict-patient/', views.predict_patient_view, name='predict-patient'),
    path('edit-profile/', views.edit_profile_view, name='edit-profile'),
]

