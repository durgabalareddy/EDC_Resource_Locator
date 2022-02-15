from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from users.models import user as User_extended
from django.shortcuts import redirect, render

from ResourceLocator.models import *

@login_required(login_url='login')
def MyResources(request):
    currentUser = request.user
    print(currentUser.email[:-16])
    if request.method == 'POST':
        del_list = request.body.decode('utf-8').split(',')
        print(del_list[0][9:del_list[0].find('">')])
        for row in del_list:
            res = Resource.objects.get(pk=row[9:row.find('">')])
            res.MarkForDeletion = False if res.MarkForDeletion else True
            res.save()
        return HttpResponse('success')
    Resource_list = Resource.objects.filter(Owner=currentUser.email[:-16])
    print(Resource_list)
    user_object = User_extended.objects.get(email=request.user.email)
    
    context = { 
        'Resource_list': Resource_list,
        'user_object':user_object
    }
    return render(request,'My_Resource/MyResource.html',context)