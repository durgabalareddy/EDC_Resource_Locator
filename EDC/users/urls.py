from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('register/', views.register, name='register-home'),
    path('login/',auth_views.LoginView.as_view(template_name = 'users/login.html'), name = 'login'),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'users/logout.html'), name = 'logout'),
    path('profile/',views.profile, name='profile-page'),
    path('',views.profile),
    path('Feedback/',views.feedback, name = 'Feedback'),
    path('UserUpdate/',views.UserUpdate, name = 'UserUpdate'),
    path('profilePasswordChange/',auth_views.PasswordChangeView.as_view(template_name = 'users/profile_password_change.html'), name='password-change'),
    path('profilePasswordChangeDone',auth_views.PasswordChangeDoneView.as_view(template_name = 'users/profile_password_change.html'), name='password_change_done')
]