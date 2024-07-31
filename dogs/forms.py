from django import forms
from .models import Dog

class DogForm(forms.ModelForm):
    
    class Meta:
        model = Dog
        fields = ['name', 'breed', 'dob', 'gender', 'size', 'energy_level', 'temperament', 'address', 'vaccination_status', 'photo', 'bio']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),  # This will use a date picker in modern browsers
        }
