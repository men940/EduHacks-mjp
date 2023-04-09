from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [

    path('', views.home, name="home"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    path('profile/<str:pk>', views.userProfile, name="user-profile"),
    path('content/<str:pk>', views.content, name="content"),
    path('profile/<str:pk>', views.userProfile, name="user-profile"),
    path('create-content/', views.createContent, name="create-content"),
    path('update-content/<str:pk>', views.updateContent, name="update-content"),
    path('delete-content/<str:pk>', views.deleteContent, name="delete-content"),
    path('delete-comment/<str:pk>', views.deleteComment, name="delete-comment"),
    path('update-user/', views.updateUser, name="update-user"),
    path('contact/', views.userMessage, name="contact"),

]
