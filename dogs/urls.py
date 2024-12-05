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
    path('dogs/profile/<int:id>/', views.view_dog_profile),

    path('catch_mouse',views.catch_mouse,name='catch_mouse'),

    path('feed',views.feed,name='feed'),
    path('post/create',views.post_create,name='post_create'),
    path('post/<int:pk>/delete/',views.post_delete,name='post_delete'),
    path('post/<int:pk>/comment_create',views.comment_create,name='comment_create'),
    path('comment/<int:pk>/delete',views.comment_delete,name='comment_delete'),
    path('post/<int:pk>/like',views.like,name='like'),
    path('get_profile_photo/<int:owner_id>',views.get_profile_photo,name='get_profile_photo'),

    path('chat/<int:dog_id>/', views.chat_view, name='chat'),
    path('send_message/', views.send_message, name='send_message'),


    #  path('ai-match/<int:dog_id>/', views.ai_match_dogs, name='ai_match_dogs'),
]
