from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('signin',views.signin,name='register'),
    path('signup',views.signup,name='signup'),
    path('logout',views.signout,name='logout'),
]
