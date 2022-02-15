from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.contrib import messages

from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.models import User, Group

from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

from .forms import UserRegisterForm, UserUpdateForm

from ResourceLocator.models import application

from Dockers.models import user as docker_user

from users.models import user as User_extended

from django.http.response import HttpResponse

from .models import *

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                messages.warning(request, f'Email already exists')
                return redirect('register-home')
            if email.split('@')[1] != 'informatica.com':
                messages.warning(request, f'Kindly Enter Informatica Email Address')
                return redirect('register-home')
            app_list = ['ResourceLocator','ScannerInfo']
            form.save()
            user = User.objects.get(username=username)
            if docker_user.objects.filter(email=email).count() > 0 :
                group = Group.objects.get(name='ISC_MM_DSG')
                user.groups.add(group)
                app_list.append('Dockers')
            app_list.append('MyAssets')
            app_list.append('Feedback')
            app_list.append('Dockers')
            app = application(user=user,apps=app_list)
            app.save()
            if User_extended.objects.filter(email=email).count() == 0:
              user_object = User_extended(FullName="",email=email,region="")
              user_object.save()
            messages.success(request, f'Account Creation successfull. Please try logging in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        if 'accchange' in request.POST:
            form = UserUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, f'Your Account has been updated')
                return redirect('profile-page')
        else:
            p_form = PasswordChangeForm(request.user, request.POST)
            if p_form.is_valid():
                user = p_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, f'Your Password has been updated')
                return redirect('profile-page')
    
    form = UserUpdateForm(instance=request.user)
    p_form = PasswordChangeForm(user=request.user)
    user_object = User_extended.objects.get(email=request.user.email)
    context = {'form':form , 'p_form':p_form, 'user_object':user_object}
    return render(request,'users/profile.html',context)

@login_required(login_url='login')
def password_change(request):
    if request.method == 'POST':
        p_form = PasswordChangeForm(request.user, request.POST)
        if p_form.is_valid():
            user = p_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password-change')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        p_form = PasswordChangeForm(user=request.user)
        user_object = User_extended.objects.get(email=request.user.email)
        context = {
        'p_form' : p_form,
        'user_object':user_object
        }
        return render(request,'users/profile_password_change.html',context)

@login_required(login_url='login')
def feedback(request):
    currentUser = request.user
    user_object = User_extended.objects.get(email=request.user.email)
    if request.method == 'POST':
        response = request.body.decode('utf-8').split(',')
        if Feedback.objects.filter(user = currentUser).count() != 0:
            feed = Feedback.objects.filter(user=currentUser).first()
            feed.HowHelped = response[0]
            feed.WhatImproved = response[1]
            feed.save()
        else:
            feed = Feedback(user=currentUser,HowHelped=response[0],WhatImproved=response[1])
            feed.save()
        return HttpResponse('success')
    
    context = {
        'Response': Feedback.objects.filter(user = currentUser).first(),
        'user_object':user_object
    }
    return render(request,'users/Feedback.html',context)

@login_required(login_url='login')
def UserUpdate(request):
    currentUser = request.user
    user_object = User_extended.objects.get(email=request.user.email)
    if request.method == 'POST':
        response = request.body.decode('utf-8').split(',')
        user_object.FullName = response[0]
        user_object.region = response[1]
        user_object.save()
        return redirect('profile-page')
