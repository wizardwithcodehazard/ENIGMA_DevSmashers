# forums/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Topic, Post, Comment
from .forms import PostForm, CommentForm # Import both forms

# View to list all topics
class ForumListView(View):
    def get(self, request):
        topics = Topic.objects.all()
        return render(request, 'forums/forum_list.html', {'topics': topics})

# View to list all posts in a specific topic
class TopicPostListView(View):
    def get(self, request, slug):
        topic = get_object_or_404(Topic, slug=slug)
        posts = Post.objects.filter(topic=topic)
        return render(request, 'forums/topic_post_list.html', {'topic': topic, 'posts': posts})

# View for a single post and its comments (UPDATED)
class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = post.comments.all()
        comment_form = CommentForm()
        
        context = {
            'post': post,
            'comments': comments,
            'comment_form': comment_form,
        }
        return render(request, 'forums/post_detail.html', context)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('post_detail', pk=pk)
        
        # If form is not valid, re-render the page with the form and its errors
        comments = post.comments.all()
        context = {
            'post': post,
            'comments': comments,
            'comment_form': comment_form,
        }
        return render(request, 'forums/post_detail.html', context)

# View to create a new post (UPDATED)
class PostCreateView(LoginRequiredMixin, View):
    def get(self, request, slug):
        topic = get_object_or_404(Topic, slug=slug)
        form = PostForm()
        return render(request, 'forums/post_create.html', {'topic': topic, 'form': form})

    def post(self, request, slug):
        topic = get_object_or_404(Topic, slug=slug)
        form = PostForm(request.POST)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
        
        # If form is not valid, re-render the page with the form and its errors
        return render(request, 'forums/post_create.html', {'topic': topic, 'form': form})