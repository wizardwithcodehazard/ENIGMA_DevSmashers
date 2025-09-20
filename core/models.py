from django.db import models
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

# ------------------------------
# Feature 1: Predictive Risk Engine
# ------------------------------

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Django Auth
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20, choices=[("M", "Male"), ("F", "Female"), ("O", "Other")])
    
    primary_condition = models.CharField(max_length=100)
    secondary_conditions = models.TextField(blank=True, null=True)
    medications = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    
    smoking_status = models.CharField(max_length=20, choices=[("Never", "Never"), ("Former", "Former"), ("Current", "Current")])
    alcohol_consumption = models.CharField(max_length=20, choices=[("None", "None"), ("Occasional", "Occasional"), ("Regular", "Regular")])

    height_cm = models.IntegerField()
    weight_kg = models.FloatField()
    blood_pressure_baseline = models.CharField(max_length=10, blank=True, null=True)
    resting_heart_rate = models.IntegerField(blank=True, null=True)
    last_hba1c = models.FloatField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)


class DailyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    log_date = models.DateField(auto_now_add=True)

    # Vitals
    systolic_bp = models.IntegerField(blank=True, null=True)
    diastolic_bp = models.IntegerField(blank=True, null=True)
    heart_rate = models.IntegerField(blank=True, null=True)
    blood_glucose = models.FloatField(blank=True, null=True)

    # Lifestyle
    sleep_hours = models.FloatField(blank=True, null=True)
    exercise_minutes = models.IntegerField(blank=True, null=True)
    steps_count = models.IntegerField(blank=True, null=True)
    diet_notes = models.TextField(blank=True, null=True)
    water_intake_liters = models.FloatField(blank=True, null=True)

    # Stress & Symptoms
    stress_level = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)

    # Medication Adherence
    medication_taken = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)


class StabilityScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score_date = models.DateTimeField(auto_now_add=True)
    score_value = models.IntegerField()  # e.g., 0-100 stability index
    risk_prediction = models.TextField()  # e.g., "High probability of hypertensive episode"
    ai_response_raw = models.JSONField()  # full response from Gemini


# ------------------------------
# Feature 2: Context-Aware Nudges
# ------------------------------

class Nudge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nudge_date = models.DateField(auto_now_add=True)
    message = models.TextField()
    context_reason = models.TextField(blank=True, null=True)  # why this nudge was given
    created_at = models.DateTimeField(auto_now_add=True)


# ------------------------------
# Feature 3: Closed-Loop Clinician Connect
# ------------------------------

class Clinician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    hospital_affiliation = models.CharField(max_length=200, blank=True, null=True)


class PatientClinician(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient_links")
    clinician = models.ForeignKey(Clinician, on_delete=models.CASCADE, related_name="clinician_links")
    created_at = models.DateTimeField(auto_now_add=True)


class PatientReport(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    clinician = models.ForeignKey(Clinician, on_delete=models.CASCADE)
    generated_at = models.DateTimeField(auto_now_add=True)

    ai_summary = models.TextField()   # readable summary for clinician
    ai_recommendations = models.JSONField()  # suggested actions
    stability_score = models.IntegerField()
    logs_snapshot = models.JSONField()  # copy of patient logs sent


class ClinicianAction(models.Model):
    report = models.ForeignKey(PatientReport, on_delete=models.CASCADE)
    clinician = models.ForeignKey(Clinician, on_delete=models.CASCADE)
    
    action_type = models.CharField(max_length=50, choices=[
        ("advice", "Advice"),
        ("prescription", "Prescription"),
        ("video_consult", "Video Consultation")
    ])
    action_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    acknowledged_by_patient = models.BooleanField(default=False)


# ------------------------------
# Feature 4: Community & Peer Support
# ------------------------------

class SupportGroup(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ("condition", "Condition-based"),
        ("lifestyle", "Lifestyle-based")
    ])
    created_at = models.DateTimeField(auto_now_add=True)


class GroupMembership(models.Model):
    group = models.ForeignKey(SupportGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)


class ForumPost(models.Model):
    group = models.ForeignKey(SupportGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_milestone = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class ForumComment(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class ForumReaction(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=20, choices=[
        ("like", "Like"), ("celebrate", "Celebrate"), ("support", "Support")
    ])
    created_at = models.DateTimeField(auto_now_add=True)


# ------------------------------
# Feature 5: Goal & Progress Dashboard
# ------------------------------

class UserGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_type = models.CharField(max_length=50, choices=[
        ("medication", "Medication Adherence"),
        ("exercise", "Exercise"),
        ("diet", "Diet"),
        ("sleep", "Sleep"),
        ("stability", "Stability Score")
    ])
    target_value = models.FloatField()
    unit = models.CharField(max_length=20)  # e.g., "hours", "days", "score"
    created_at = models.DateTimeField(auto_now_add=True)


class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    achieved_at = models.DateTimeField(auto_now_add=True)


