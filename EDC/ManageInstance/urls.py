from django.urls import path

from . import views


urlpatterns = [
    path('ManageInstance/', views.manage, name = 'ManageInstance'),
    path('start',views.start, name='start'),
    path('stop',views.stop, name='stop'),
]