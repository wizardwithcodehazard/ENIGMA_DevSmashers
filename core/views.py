from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import (
    UserProfile, DailyLog, StabilityScore, Nudge, ClinicianAction,
    ForumPost, UserGoal, Achievement, SupportGroup, GroupMembership,
    Clinician
)
from .forms import UserProfileForm, DailyLogForm
import requests
import json
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime

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

    # Recent Daily Logs (last 7 days)
    from datetime import date, timedelta
    week_ago = date.today() - timedelta(days=7)
    recent_daily_logs = DailyLog.objects.filter(user=user, log_date__gte=week_ago).order_by('-log_date')[:7]

    context = {
        "profile": profile,
        "latest_log": latest_log,
        "stability": stability,
        "nudge": nudge,
        "clinician_actions": clinician_actions,
        "posts": posts,
        "goals": goals,
        "achievements": achievements,
        "recent_daily_logs": recent_daily_logs,
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


# --------------------------
# Daily Log Views
# --------------------------

@login_required
def daily_log_create(request):
    """Create or update today's daily log"""
    from datetime import date
    
    today = date.today()
    
    # Check if user already has a log for today
    try:
        daily_log = DailyLog.objects.get(user=request.user, log_date=today)
        # If log exists, redirect to edit
        return redirect('core:daily-log-edit', log_id=daily_log.id)
    except DailyLog.DoesNotExist:
        daily_log = None
    
    if request.method == 'POST':
        form = DailyLogForm(request.POST, instance=daily_log)
        if form.is_valid():
            daily_log = form.save(commit=False)
            daily_log.user = request.user
            daily_log.log_date = today
            daily_log.save()
            messages.success(request, 'Daily log saved successfully!')
            return redirect('core:daily-log-list')
    else:
        form = DailyLogForm(instance=daily_log)
    
    context = {
        'form': form,
        'daily_log': daily_log,
        'today': today,
    }
    return render(request, 'daily_log_create.html', context)


@login_required
def daily_log_edit(request, log_id):
    """Edit an existing daily log"""
    try:
        daily_log = DailyLog.objects.get(id=log_id, user=request.user)
    except DailyLog.DoesNotExist:
        messages.error(request, 'Daily log not found.')
        return redirect('core:daily-log-list')
    
    if request.method == 'POST':
        form = DailyLogForm(request.POST, instance=daily_log)
        if form.is_valid():
            form.save()
            messages.success(request, 'Daily log updated successfully!')
            return redirect('core:daily-log-list')
    else:
        form = DailyLogForm(instance=daily_log)
    
    context = {
        'form': form,
        'daily_log': daily_log,
    }
    return render(request, 'daily_log_edit.html', context)


@login_required
def daily_log_list(request):
    """List all daily logs for the user"""
    daily_logs = DailyLog.objects.filter(user=request.user).order_by('-log_date')
    
    context = {
        'daily_logs': daily_logs,
    }
    return render(request, 'daily_log_list.html', context)


@login_required
def daily_log_detail(request, log_id):
    """View details of a specific daily log"""
    try:
        daily_log = DailyLog.objects.get(id=log_id, user=request.user)
    except DailyLog.DoesNotExist:
        messages.error(request, 'Daily log not found.')
        return redirect('core:daily-log-list')
    
    context = {
        'daily_log': daily_log,
    }
    return render(request, 'daily_log_detail.html', context)



@login_required
def goal_dashboard_view(request):
    """
    Render the Goal & Progress Dashboard page.
    The front-end will call `goal_data_api` to fetch the JSON used to render charts and heatmap.
    """
    return render(request, "goal.html")




@login_required
def goal_data_api(request):
    """
    Returns:
    {
      "logs": [ {date, systolic_bp, ...}, ... ]  # last 7 days for charts
      "monthly_data": { "2025-09-01": 2, "2025-09-02": 0, ... }  # activity levels for heatmap
      "max_streak": int,
      "current_streak": int,
      "monthly_active_count": int,
      "ai_summary": dict_or_error
    }
    """
    user = request.user
    today = datetime.date.today()

    # --- Monthly Data for GitHub-style Heatmap ---
    first_day_of_month = today.replace(day=1)
    if today.month == 12:
        last_day_of_month = datetime.date(today.year + 1, 1, 1) - datetime.timedelta(days=1)
    else:
        last_day_of_month = datetime.date(today.year, today.month + 1, 1) - datetime.timedelta(days=1)

    monthly_logs = DailyLog.objects.filter(
        user=user,
        log_date__gte=first_day_of_month,
        log_date__lte=last_day_of_month
    )

    monthly_data = {}
    monthly_active_count = 0

    for log in monthly_logs:
        # Count logged health metrics (include new fields)
        activity_fields = [
            log.weight_kg, log.systolic_bp, log.diastolic_bp, log.heart_rate,
            log.blood_glucose, log.temperature, log.sleep_hours, log.exercise_minutes,
            log.steps_count, log.water_intake_liters, log.stress_level, log.mood_rating,
            log.symptoms, log.diet_notes, log.notes
        ]
        activity_count = sum(1 for field in activity_fields if field not in (None, "", []))
        if log.medication_taken:
            activity_count += 1

        # Convert to 0-4 scale for heatmap colors
        if activity_count == 0:
            activity_level = 0
        elif activity_count <= 2:
            activity_level = 1
        elif activity_count <= 4:
            activity_level = 2
        elif activity_count <= 6:
            activity_level = 3
        else:
            activity_level = 4

        date_str = log.log_date.strftime("%Y-%m-%d")
        monthly_data[date_str] = activity_level

        if activity_level > 0:
            monthly_active_count += 1

    # --- Last 7 Days Data for Charts ---
    start_date = today - datetime.timedelta(days=6)
    logs_qs = DailyLog.objects.filter(user=user, log_date__gte=start_date, log_date__lte=today).order_by("log_date")
    logs_by_date = {log.log_date: log for log in logs_qs}

    logs_list = []
    for i in range(7):
        d = start_date + datetime.timedelta(days=i)
        log = logs_by_date.get(d)
        logs_list.append({
            "date": d.strftime("%Y-%m-%d"),
            "weight_kg": log.weight_kg if log else None,
            "systolic_bp": log.systolic_bp if log else None,
            "diastolic_bp": log.diastolic_bp if log else None,
            "heart_rate": log.heart_rate if log else None,
            "blood_glucose": log.blood_glucose if log else None,
            "temperature": log.temperature if log else None,
            "sleep_hours": log.sleep_hours if log else None,
            "exercise_minutes": log.exercise_minutes if log else None,
            "steps_count": log.steps_count if log else None,
            "water_intake": log.water_intake_liters if log else None,
            "stress_level": log.stress_level if log else None,
            "mood_rating": log.mood_rating if log else None,
            "symptoms": log.symptoms if log else None,
            "diet_notes": log.diet_notes if log else None,
            "notes": log.notes if log else None,
            "medication_taken": log.medication_taken if log else False,
        })

    # --- Streak Calculations ---
    all_logs_qs = DailyLog.objects.filter(user=user).order_by("log_date")
    logged_dates = set()

    for log in all_logs_qs:
        has_data = any([
            log.weight_kg, log.systolic_bp, log.diastolic_bp, log.heart_rate,
            log.blood_glucose, log.temperature, log.sleep_hours, log.exercise_minutes,
            log.steps_count, log.water_intake_liters, log.stress_level, log.mood_rating,
            log.symptoms, log.diet_notes, log.notes, log.medication_taken
        ])
        if has_data:
            logged_dates.add(log.log_date)

    all_dates = sorted(logged_dates)

    # Max streak calculation
    max_streak = 0
    current_streak_count = 0
    prev_date = None

    for date in all_dates:
        if prev_date is None:
            current_streak_count = 1
        else:
            if (date - prev_date).days == 1:
                current_streak_count += 1
            else:
                current_streak_count = 1
        max_streak = max(max_streak, current_streak_count)
        prev_date = date

    # Current streak: count backwards from today
    current_streak = 0
    check_date = today
    while check_date in logged_dates:
        current_streak += 1
        check_date -= datetime.timedelta(days=1)

    # --- AI Summary via Groq ---
    ai_summary = {}
    try:
        GROQ_API_KEY = "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"
        if not GROQ_API_KEY or GROQ_API_KEY == "YOUR_GROQ_KEY":
            ai_summary = {"error": "Groq API key not configured"}
        else:
            simplified_logs = []
            for item in logs_list:
                simplified = {k: v for k, v in item.items() if v is not None and k not in ["date"]}
                if simplified:
                    simplified_logs.append({"date": item["date"], "data": simplified})

            if not simplified_logs:
                ai_summary = {"summary": "No health data logged in the past 7 days. Start tracking your daily health metrics!"}
            else:
                prompt = f"""
You are a health coach AI for an Indian audience.
Analyze the last 7 days of health data and return JSON with these exact keys:
- "summary": brief paragraph about overall trends
- "praise": 1-2 positive points about good habits
- "warnings": 1-2 concerns or areas needing attention  
- "suggestions": 2-3 specific actionable recommendations

Return only valid JSON, no markdown.

Health Data: {json.dumps(simplified_logs, indent=2)}
Monthly Stats: {monthly_active_count} active days, Current streak: {current_streak} days.
"""

                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1,
                    "max_tokens": 500
                }

                response = requests.post(url, headers=headers, json=payload, timeout=20)
                response.raise_for_status()

                llm_output = response.json()["choices"][0]["message"]["content"]
                cleaned = re.sub(r"```json|```", "", llm_output).strip()

                try:
                    ai_summary = json.loads(cleaned)
                except json.JSONDecodeError:
                    ai_summary = {"summary": cleaned}

    except Exception as e:
        ai_summary = {"error": f"AI analysis failed: {str(e)}"}

    return JsonResponse({
        "logs": logs_list,
        "monthly_data": monthly_data,
        "max_streak": max_streak,
        "current_streak": current_streak,
        "monthly_active_count": monthly_active_count,
        "ai_summary": ai_summary
    })
