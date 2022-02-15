from django.urls import path
from .CoreLogic import *
from . import views


urlpatterns = [
    path('Dockers/', views.Dockers, name = 'Dockers' ),
    path('MyDockers/', views.MyDockers, name = 'MyDockers'),
    path('MyDockers/edit/<int:id>/', views.DockerEdit, name = 'DockerEdit')
]

start_schedular()