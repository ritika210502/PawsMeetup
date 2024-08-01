from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('add/',views.add_dog,name='add_dog'),
    path('dog_list/',views.dog_list,name='dog_list'),

    path('ai-match/<int:dog_id>/', views.ai_match_dogs, name='ai_match_dogs'),
]
