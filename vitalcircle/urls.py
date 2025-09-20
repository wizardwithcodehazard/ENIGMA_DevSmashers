from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),  # Include users app urls (login/logout/register)
    path('forums/', include('forums.urls')),  # Include forums app urls (forum, topic, post)
    path('', include('core.urls')),  # Include core app urls (home, dashboard)
]
