# forums/admin.py

from django.contrib import admin
from .models import Topic, Post, Comment

# Register your models here.
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Comment)