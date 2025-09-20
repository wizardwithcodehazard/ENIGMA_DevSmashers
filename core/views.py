from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import (
    UserProfile, DailyLog, StabilityScore, Nudge, ClinicianAction,
    ForumPost, UserGoal, Achievement, SupportGroup, GroupMembership,
    Clinician
)
from .forms import UserProfileForm
import requests
import json
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
    
    # Check if user profile is filled
    try:
        profile = UserProfile.objects.get(user=user)
        if not profile.is_filled:
            return redirect('core:complete-profile')
    except UserProfile.DoesNotExist:
        return redirect('core:complete-profile')

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

# --------------------------
# Stability Score Views
# --------------------------

@csrf_exempt
def predict_patient_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)


    try:
        # Parse input JSON
        patient_data = json.loads(request.body.decode("utf-8"))


        # Groq API
        GROQ_API_KEY = "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"
        url = "https://api.groq.com/openai/v1/chat/completions"


        # Prompt with escaped braces
        prompt = f"""
You are an experienced healthcare assistant AI with over 10 years of experience explaining health insights to the general public in India.


Task:
- Analyze the patient data below.
- Return a JSON object with two fields:
  1. "stability_score": an integer between 0-100 reflecting the overall health stability of the patient.
  2. "risk_prediction": a short, easy-to-understand explanation (3-4 lines) of potential health risks for a layman. Include possible causes from lifestyle, vitals, and medications.


Additional Instructions:
- Provide the explanation in simple English (layman-friendly, India context) and a Hinglish version.
- Respond ONLY in JSON.
- Use the following JSON template (escape braces for Python f-string):


{{
  "stability_score": 0,
  "risk_prediction": {{
      "english": "...",
      "hinglish": "..."
  }}
}}


Patient data:
{json.dumps(patient_data, indent=2)}
"""


        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}]
        }


        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()


        llm_output = data["choices"][0]["message"]["content"]
        cleaned = re.sub(r"```json|```", "", llm_output).strip()


        # ---- FIX: Parse inner JSON if it's returned as string ----
        try:
            parsed = json.loads(cleaned)
            # If risk_prediction is still a string, try parsing it again
            if isinstance(parsed.get("risk_prediction"), str):
                try:
                    parsed["risk_prediction"] = json.loads(parsed["risk_prediction"])
                except:
                    pass  # fallback: keep as string
            result = parsed
        except json.JSONDecodeError:
            # fallback
            result = {"stability_score": None, "risk_prediction": cleaned}


        return JsonResponse(result)


    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON input."}, status=400)
    except requests.exceptions.HTTPError as e:
        return JsonResponse({"error": f"HTTP Error: {str(e)}"}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)




def stability_view(request):
    """
    Render the stability.html page where the user can fill patient data
    and check health stability.
    """
    # Get user profile data to pre-fill the form
    profile = None
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            profile = None
    
    context = {
        'profile': profile,
    }
    return render(request, "stability.html", context)

# --------------------------
# Profile Management Views
# --------------------------

@login_required
def complete_profile_view(request):
    """Complete user profile - required after registration"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.is_filled = True
            profile.save()
            messages.success(request, 'Profile completed successfully! You can now access all features.')
            return redirect('core:user-dashboard')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'complete_profile.html', context)

@login_required
def edit_profile_view(request):
    """Edit user profile information"""
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user, is_filled=False)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.is_filled = True
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('core:user-dashboard')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'edit_profile.html', context)