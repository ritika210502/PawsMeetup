from django import forms
from .models import Dog

class DogForm(forms.ModelForm):
    
    class Meta:
        model = Dog
        fields = ['name', 'breed', 'dob', 'gender', 'size', 'energy_level', 'temperament', 'address', 'vaccination_status', 'photo', 'bio']
