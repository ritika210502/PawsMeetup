from django import forms
from .models import Dog,Post,Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


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

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username']

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['content','image','video']
        
    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        video = cleaned_data.get('video')

        # Check if both fields are populated
        if image and video:
            raise ValidationError("You can only upload either an image or a video, not both.")

        return cleaned_data

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['content']