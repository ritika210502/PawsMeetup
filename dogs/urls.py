from django.urls import path
from . import views

urlpatterns = [
    path('add/',views.add_dog,name='add_dog'),
    path('',views.dog_list,name='dog_list'),
    path('ai-match/<int:dog_id>/', views.ai_match_dogs, name='ai_match_dogs'),
]
