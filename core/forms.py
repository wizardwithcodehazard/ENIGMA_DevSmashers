from django import forms
from .models import UserProfile

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
