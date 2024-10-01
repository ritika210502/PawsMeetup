from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('healthcare',views.healthcare,name="healthcare"),
    path('training',views.training,name="training"),
    path('add/',views.add_dog,name='add_dog'),
    path('dog_list/',views.dog_list,name='dog_list'),
    path('ai-match_dogs/', views.ai_match_dogs, name='ai_match_dogs'),
    path('edit_dog/<int:dog_id>/',views.edit_dog,name='edit_dog'),
    path('delete_dog/<int:dog_id>/',views.delete_dog,name='delete_dog'),
    path('dogs/profile/<int:id>/', views.view_dog_profile, name='view_dog_profile'),
    path('catch_mouse',views.catch_mouse,name='catch_mouse'),

    #  path('ai-match/<int:dog_id>/', views.ai_match_dogs, name='ai_match_dogs'),
]
