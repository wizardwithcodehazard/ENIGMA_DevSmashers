# forums/urls.py

from django.urls import path
from .views import ForumListView, TopicPostListView, PostDetailView, PostCreateView

urlpatterns = [
    path('', ForumListView.as_view(), name='forum_list'),
    path('topic/<slug:slug>/', TopicPostListView.as_view(), name='topic_post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('topic/<slug:slug>/new/', PostCreateView.as_view(), name='post_create'),
]