from django import VERSION
from django.contrib.auth.decorators import login_required
from django.http import response
from django.http.response import StreamingHttpResponse
from django.shortcuts import render
from users.models import user as User_extended
import subprocess

from .models import *

from ResourceLocator.models import Instance

@login_required(login_url='login')
def manage(request):
    instances = Instance.objects.filter(REGION='ISC').order_by('VERSION')
    user_object = User_extended.objects.get(email=request.user.email)
    context = {
        'instances' : instances,
        'user_object':user_object
    }
    return render(request,'ManageInstance/ManageInstance.html',context)


@login_required(login_url='login')
def start(request):
    print(request.body.decode('utf-8'))
    StartCommand = ManageInstance.objects.filter(ins=Instance.objects.get(VERSION=request.body.decode('utf-8')))[0]
    print(StartCommand.startCMD)
    def inner():
        command = 'timeout 2m sh /data/users/infadsg/EDC_Resource_Locator/start.sh '+StartCommand.startCMD
        proc = subprocess.Popen(
                ['sshpass -p infadsg@2020 ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 infadsg@inglxbdm04 '+command],
                shell=True,
                executable='/bin/sh',
                stdout=subprocess.PIPE
                )
        count = 0
        for line in iter(proc.stdout.readline,''):
            if count > 33:
                yield line.rstrip() + b'\n'
            else:
                count = count + 1

    return StreamingHttpResponse(inner())

@login_required(login_url='login')
def stop(request):
    StopCommand = ManageInstance.objects.filter(ins=Instance.objects.get(VERSION=request.body.decode('utf-8')))[0]
    def inner():
        command = 'timeout 2m sh /data/users/infadsg/EDC_Resource_Locator/stop.sh '+StopCommand.stopCMD
        proc = subprocess.Popen(
                ['sshpass -p infadsg@2020 ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 infadsg@inglxbdm04 '+command],
                shell=True,
                executable='/bin/sh',
                stdout=subprocess.PIPE
                )
        count = 0
        for line in iter(proc.stdout.readline,''):
            if count > 33:
                yield line.rstrip() + b'\n'
            else:
                count = count + 1

    return StreamingHttpResponse(inner())
