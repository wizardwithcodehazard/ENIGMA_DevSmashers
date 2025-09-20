from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name="login" ),
    path('logout/', views.logout_view, name="logout" ),
    path('doctor-register/', views.doctor_register, name='doctor_register'),
    path('user-register/', views.user_register, name='user_register'),
    

] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

