from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib.auth.models import User
from users.models import user as User_extended
import logging

logger = logging.getLogger('ResourceLocator')

@login_required(login_url='login')
def home(request):
    user = request.user
    apps = application.objects.filter(user=user)[0].apps
    search_count = Search_count.objects.get(id=1)
    search_count.search_count = search_count.search_count + 1
    search_count.save()
    instances = Instance.objects.order_by('VERSION')
    if request.method == 'POST':
        form = ResourceTypeSelectionForm(request.POST)
        if form.is_valid():
            resource_type = form.cleaned_data.get('Resource_Type')
    else:
        form = ResourceTypeSelectionForm()
        resource_type = Resource_Type.objects.order_by('resource_type')[0]
    Resource_types = Resource_Type.objects.order_by('resource_type')
    r_t = Resource_Type.objects.get(resource_type=resource_type)
    logger.info("User {} searched for resource type {}".format(user.email,r_t.resource_type))
    Resource_list = Resource.objects.filter(Resource_Type=r_t)
    resource_count = {}
    for instance in instances:
        resource_count[instance] = Resource_list.filter(ins=instance).count()
    user_object = User_extended.objects.get(email=request.user.email)
    context = { 
        "form":form,
        'instances' : instances,
        'resource_count':resource_count,
        'resource_type': resource_type,
        'Resource_list': Resource_list,
        'search_count': search_count,
        'user_object' : user_object

    }
    return render(request,'ResourceLocator/ResourceLocator.html',context)

@login_required(login_url='login')
def scanner_info_view(request):
    FullName = User_extended.objects.get(email=request.user.email).FullName
    Scanner_info = Resource_Type.objects.order_by('resource_type')
    context = { 
      'Scanner_info': Scanner_info,
      'FullName': FullName
      }
    return render(request,'ResourceLocator/scannerInfo.html',context)

@login_required(login_url='login')
def Search(request):
    return redirect('/ResourceLocator/')
    
@login_required(login_url='login')
def ScanEdit(request, id):
    scanner = Resource_Type.objects.get(id=id)
    if request.method == 'POST':
        form = ScannerEditForm(request.POST,instance=scanner)
        if form.is_valid():
            form.save()
            return redirect('scannerinfo')
    form = ScannerEditForm(instance=scanner)
    user_object = User_extended.objects.get(email=request.user.email)
    context = { 
        "form":form,
        'user_object':user_object
    }
    return render(request,'ResourceLocator/scanneredit.html',context)