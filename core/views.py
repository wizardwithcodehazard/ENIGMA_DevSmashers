from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import (
    UserProfile, DailyLog, StabilityScore, Nudge, ClinicianAction,
    ForumPost, UserGoal, Achievement, SupportGroup, GroupMembership,
    Clinician
)

# --------------------------
# Home View
# --------------------------

def home_view(request):
    """Home page view - shows landing page for unauthenticated users"""
    if request.user.is_authenticated:
        # Redirect authenticated users to their appropriate dashboard
        if request.user.is_doctor:
            return redirect('core:doctor-dashboard')
        elif request.user.is_user:
            return redirect('core:user-dashboard')
    return render(request, 'home.html')

# --------------------------
# Dashboard View
# --------------------------

@login_required
def dashboard_view(request):
    user = request.user
    profile = UserProfile.objects.filter(user=user).first()

    # Latest Daily Log
    latest_log = DailyLog.objects.filter(user=user).order_by('-log_date').first()

    # Latest Stability Score
    stability = StabilityScore.objects.filter(user=user).order_by('-score_date').first()

    # Today's Nudge
    nudge = Nudge.objects.filter(user=user).order_by('-nudge_date').first()

    # Recent Clinician Actions
    clinician_actions = ClinicianAction.objects.filter(clinician__user=user).order_by('-created_at')[:5]

    # Community Highlights (recent forum posts)
    groups = GroupMembership.objects.filter(user=user).values_list('group', flat=True)
    posts = ForumPost.objects.filter(group__in=groups).order_by('-created_at')[:5]

    # User Goals & Achievements
    goals = UserGoal.objects.filter(user=user)
    achievements = Achievement.objects.filter(user=user).order_by('-achieved_at')[:5]

    context = {
        "profile": profile,
        "latest_log": latest_log,
        "stability": stability,
        "nudge": nudge,
        "clinician_actions": clinician_actions,
        "posts": posts,
        "goals": goals,
        "achievements": achievements,
    }

    return render(request, "user-dashboard.html", context)

@login_required
def doctor_dashboard_view(request):
    user = request.user
    profile = Clinician.objects.filter(user=user).first()
    context = {
        "profile": profile,
    }
    return render(request, "doctor-dashboard.html")