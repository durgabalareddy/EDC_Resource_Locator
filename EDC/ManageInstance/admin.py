from django.contrib import admin

from .models import *

class ManageInstanceView(admin.ModelAdmin):
    list_display = ('id','ins', 'startCMD', 'stopCMD')

admin.site.register(ManageInstance,ManageInstanceView)
