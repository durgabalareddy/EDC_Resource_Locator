from django.contrib import admin

from .models import *

class DockerView(admin.ModelAdmin):
    list_display = ('id','CaseNo', 'Host', 'Version','email','pVersion', 'createdDate', 'Visibilty', 'Note')

class userView(admin.ModelAdmin):
    list_display = ('id','username', 'email', 'region')

admin.site.register(dockers,DockerView)

admin.site.register(user,userView)