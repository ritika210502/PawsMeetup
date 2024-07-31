from django.urls import path
from . import views

urlpatterns = [
    path('add/',views.add_dog,name='add_dog'),
    path('',views.dog_list,name='dog_list'),
]
