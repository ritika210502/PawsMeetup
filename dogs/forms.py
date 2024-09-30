from django import forms
from .models import Dog
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = ['name', 'breed', 'dob', 'gender', 'size', 'energy_level', 'temperament', 'address', 'vaccination_status', 'photo', 'bio']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),  # This will use a date picker in modern browsers
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']  # Save the email
        if commit:
            user.save()
        return user
