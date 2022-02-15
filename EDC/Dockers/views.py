from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from .models import dockers, user

from .forms import *

from users.models import user as User_extended

import logging

logger = logging.getLogger('Docker')

@login_required(login_url='login')
def Dockers(request):
    currentUser = request.user
    logger.info("User {} accessed Dockers".format(currentUser.email))
    region = User_extended.objects.get(email=currentUser.email).region
    docker = dockers.objects.filter(region=region)
    user_object = User_extended.objects.get(email=request.user.email)
    context = { 
        'Dockers': docker,
        'user_object':user_object
    }
    return render(request,'Dockers/Dockers.html',context)


@login_required(login_url='login')
def MyDockers(request):
    currentUser = request.user
    Docker_list = dockers.objects.filter(email=currentUser.email)
    user_object = User_extended.objects.get(email=request.user.email)
    context = { 
        'Dockers': Docker_list,
        'user_object':user_object
    }
    return render(request,'Dockers/MyDockers.html',context)

@login_required(login_url='login')
def DockerEdit(request, id):
    docker = dockers.objects.get(id=id)
    user_object = User_extended.objects.get(email=request.user.email)
    if request.method == 'POST':
        form = DockerEditForm(request.POST,instance=docker)
        if form.is_valid():
            form.save()
            return redirect('MyDockers')
    form = DockerEditForm(instance=docker)
    context = { 
        "form":form,
        'user_object':user_object
    }
    return render(request,'Dockers/dockeredit.html',context)
