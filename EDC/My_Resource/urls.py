from django.urls import path

from . import views

from .CoreLogic import *


urlpatterns = [
    path('MyResources/', views.MyResources, name = 'MyResources')
]

start_scheduler()