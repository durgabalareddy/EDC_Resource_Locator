from django.urls import path

from django.shortcuts import redirect

from . import views

from .CoreLogic import *


urlpatterns = [
    path('ResourceLocator/', views.home, name = 'home-page'),
    path('ScannerInfo/', views.scanner_info_view, name='scannerinfo'),
    path('Search/', views.Search),
    path('ScannerInfo/edit/<int:id>/',views.ScanEdit, name='scanedit')
    
]

#get_ldm_status()
#get_resource_list()
start_schedular()