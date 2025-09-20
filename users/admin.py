# Register your models here.
from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_user', 'is_doctor', 'is_admin')  # Fields to display
    list_filter = ('is_user', 'is_doctor', 'is_admin')  # Add filters for roles
    search_fields = ('username', 'email')  # Enable search functionality

admin.site.register(User, UserAdmin)