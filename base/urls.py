from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutPage, name='logout'),
    path('login/', views.loginPage, name='login'),

    path('', views.home, name='home'),
    path('topics/', views.mobileTopic, name='topic'),
    path('activity/', views.mobileActivity, name='activity'),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name='profile'),
    
    
    # Forms
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),
    path('delete-message/<str:pk>/', views.deleteMessage, name='delete-message'),
    path('update-profile/<str:pk>/', views.updateProfile, name='update-profile'),
]

