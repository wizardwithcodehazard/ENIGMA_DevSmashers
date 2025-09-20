from django import forms
from .models import UserProfile, DailyLog

class UserProfileForm(forms.ModelForm):
    """Form for editing user profile information"""
    
    class Meta:
        model = UserProfile
        fields = [
            'date_of_birth',
            'gender',
            'primary_condition',
            'secondary_conditions',
            'medications',
            'allergies',
            'smoking_status',
            'alcohol_consumption',
            'height_cm',
            'weight_kg',
            'blood_pressure_baseline',
            'resting_heart_rate',
            'last_hba1c',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select'
            }),
            'primary_condition': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Diabetes, Hypertension'
            }),
            'secondary_conditions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter other health conditions, separated by commas'
            }),
            'medications': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter current medications, separated by commas'
            }),
            'allergies': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter known allergies, separated by commas'
            }),
            'smoking_status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'alcohol_consumption': forms.Select(attrs={
                'class': 'form-select'
            }),
            'height_cm': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Height in centimeters'
            }),
            'weight_kg': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Weight in kilograms',
                'step': '0.1'
            }),
            'blood_pressure_baseline': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 120/80'
            }),
            'resting_heart_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Resting heart rate (BPM)'
            }),
            'last_hba1c': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last HbA1c percentage',
                'step': '0.1'
            }),
        }
        labels = {
            'date_of_birth': 'Date of Birth',
            'gender': 'Gender',
            'primary_condition': 'Primary Health Condition',
            'secondary_conditions': 'Other Health Conditions',
            'medications': 'Current Medications',
            'allergies': 'Known Allergies',
            'smoking_status': 'Smoking Status',
            'alcohol_consumption': 'Alcohol Consumption',
            'height_cm': 'Height (cm)',
            'weight_kg': 'Weight (kg)',
            'blood_pressure_baseline': 'Baseline Blood Pressure',
            'resting_heart_rate': 'Resting Heart Rate (BPM)',
            'last_hba1c': 'Last HbA1c (%)',
        }
        help_texts = {
            'secondary_conditions': 'List any other health conditions you have, separated by commas.',
            'medications': 'List all current medications you are taking, separated by commas.',
            'allergies': 'List any known allergies you have, separated by commas.',
            'blood_pressure_baseline': 'Enter your typical blood pressure reading (e.g., 120/80).',
            'resting_heart_rate': 'Your heart rate when at rest (beats per minute).',
            'last_hba1c': 'Your most recent HbA1c test result as a percentage.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make all fields optional except date_of_birth
        for field_name, field in self.fields.items():
            if field_name != 'date_of_birth':
                field.required = False
                
        # Add form validation
        self.fields['height_cm'].widget.attrs['min'] = '50'
        self.fields['height_cm'].widget.attrs['max'] = '300'
        self.fields['weight_kg'].widget.attrs['min'] = '20'
        self.fields['weight_kg'].widget.attrs['max'] = '300'
        self.fields['resting_heart_rate'].widget.attrs['min'] = '30'
        self.fields['resting_heart_rate'].widget.attrs['max'] = '200'
        self.fields['last_hba1c'].widget.attrs['min'] = '3.0'
        self.fields['last_hba1c'].widget.attrs['max'] = '20.0'

    def clean_height_cm(self):
        height = self.cleaned_data.get('height_cm')
        if height is not None and (height < 50 or height > 300):
            raise forms.ValidationError('Height must be between 50 and 300 cm.')
        return height

    def clean_weight_kg(self):
        weight = self.cleaned_data.get('weight_kg')
        if weight is not None and (weight < 20 or weight > 300):
            raise forms.ValidationError('Weight must be between 20 and 300 kg.')
        return weight

    def clean_resting_heart_rate(self):
        heart_rate = self.cleaned_data.get('resting_heart_rate')
        if heart_rate is not None and (heart_rate < 30 or heart_rate > 200):
            raise forms.ValidationError('Resting heart rate must be between 30 and 200 BPM.')
        return heart_rate

    def clean_last_hba1c(self):
        hba1c = self.cleaned_data.get('last_hba1c')
        if hba1c is not None and (hba1c < 3.0 or hba1c > 20.0):
            raise forms.ValidationError('HbA1c must be between 3.0 and 20.0%.')
        return hba1c


class DailyLogForm(forms.ModelForm):
    """Form for creating and editing daily health logs"""
    
    class Meta:
        model = DailyLog
        fields = [
            'weight_kg',
            'systolic_bp',
            'diastolic_bp',
            'heart_rate',
            'blood_glucose',
            'temperature',
            'sleep_hours',
            'exercise_minutes',
            'steps_count',
            'water_intake_liters',
            'stress_level',
            'mood_rating',
            'symptoms',
            'diet_notes',
            'notes',
            'medication_taken',
        ]
        widgets = {
            'weight_kg': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Weight in kg',
                'step': '0.1'
            }),
            'systolic_bp': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Systolic BP',
                'min': '50',
                'max': '250'
            }),
            'diastolic_bp': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Diastolic BP',
                'min': '30',
                'max': '150'
            }),
            'heart_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Heart rate (BPM)',
                'min': '30',
                'max': '200'
            }),
            'blood_glucose': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Blood glucose (mg/dL)',
                'step': '0.1',
                'min': '50',
                'max': '500'
            }),
            'temperature': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Temperature (°F)',
                'step': '0.1',
                'min': '95',
                'max': '110'
            }),
            'sleep_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Hours of sleep',
                'step': '0.5',
                'min': '0',
                'max': '24'
            }),
            'exercise_minutes': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Exercise minutes',
                'min': '0',
                'max': '480'
            }),
            'steps_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Steps taken',
                'min': '0',
                'max': '50000'
            }),
            'water_intake_liters': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Water intake (liters)',
                'step': '0.1',
                'min': '0',
                'max': '10'
            }),
            'stress_level': forms.Select(attrs={
                'class': 'form-select'
            }),
            'mood_rating': forms.Select(attrs={
                'class': 'form-select'
            }),
            'symptoms': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe any symptoms you experienced today'
            }),
            'diet_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notes about your diet today'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes about your day'
            }),
            'medication_taken': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'weight_kg': 'Weight (kg)',
            'systolic_bp': 'Systolic Blood Pressure',
            'diastolic_bp': 'Diastolic Blood Pressure',
            'heart_rate': 'Heart Rate (BPM)',
            'blood_glucose': 'Blood Glucose (mg/dL)',
            'temperature': 'Temperature (°F)',
            'sleep_hours': 'Sleep Hours',
            'exercise_minutes': 'Exercise (minutes)',
            'steps_count': 'Steps Count',
            'water_intake_liters': 'Water Intake (liters)',
            'stress_level': 'Stress Level (1-5)',
            'mood_rating': 'Mood Rating (1-10)',
            'symptoms': 'Symptoms',
            'diet_notes': 'Diet Notes',
            'notes': 'Notes',
            'medication_taken': 'Medication Taken Today',
        }
        help_texts = {
            'stress_level': 'Rate your stress level from 1 (very low) to 5 (very high)',
            'mood_rating': 'Rate your mood from 1 (very poor) to 10 (excellent)',
            'symptoms': 'Describe any symptoms, discomfort, or changes you noticed today',
            'diet_notes': 'Notes about what you ate and drank today',
            'notes': 'Any additional observations or notes about your health today',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make all fields optional
        for field_name, field in self.fields.items():
            field.required = False
            
        # Add choices for stress level and mood rating
        self.fields['stress_level'].choices = [('', 'Select stress level')] + [(i, i) for i in range(1, 6)]
        self.fields['mood_rating'].choices = [('', 'Select mood rating')] + [(i, i) for i in range(1, 11)]

    def clean_systolic_bp(self):
        systolic = self.cleaned_data.get('systolic_bp')
        if systolic is not None and (systolic < 50 or systolic > 250):
            raise forms.ValidationError('Systolic blood pressure must be between 50 and 250.')
        return systolic

    def clean_diastolic_bp(self):
        diastolic = self.cleaned_data.get('diastolic_bp')
        if diastolic is not None and (diastolic < 30 or diastolic > 150):
            raise forms.ValidationError('Diastolic blood pressure must be between 30 and 150.')
        return diastolic

    def clean_heart_rate(self):
        heart_rate = self.cleaned_data.get('heart_rate')
        if heart_rate is not None and (heart_rate < 30 or heart_rate > 200):
            raise forms.ValidationError('Heart rate must be between 30 and 200 BPM.')
        return heart_rate

    def clean_blood_glucose(self):
        glucose = self.cleaned_data.get('blood_glucose')
        if glucose is not None and (glucose < 50 or glucose > 500):
            raise forms.ValidationError('Blood glucose must be between 50 and 500 mg/dL.')
        return glucose

    def clean_temperature(self):
        temp = self.cleaned_data.get('temperature')
        if temp is not None and (temp < 95 or temp > 110):
            raise forms.ValidationError('Temperature must be between 95 and 110°F.')
        return temp

    def clean_sleep_hours(self):
        sleep = self.cleaned_data.get('sleep_hours')
        if sleep is not None and (sleep < 0 or sleep > 24):
            raise forms.ValidationError('Sleep hours must be between 0 and 24.')
        return sleep

    def clean_exercise_minutes(self):
        exercise = self.cleaned_data.get('exercise_minutes')
        if exercise is not None and (exercise < 0 or exercise > 480):
            raise forms.ValidationError('Exercise minutes must be between 0 and 480.')
        return exercise

    def clean_water_intake_liters(self):
        water = self.cleaned_data.get('water_intake_liters')
        if water is not None and (water < 0 or water > 10):
            raise forms.ValidationError('Water intake must be between 0 and 10 liters.')
        return water
