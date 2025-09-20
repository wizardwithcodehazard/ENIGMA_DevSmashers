from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),  # Include users app urls (login/logout/register)
    path('', include('core.urls')),  # Include core app urls (home, dashboard)
]
