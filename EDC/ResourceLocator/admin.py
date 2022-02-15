from django.contrib import admin

from .models import *

class InstanceView(admin.ModelAdmin):
    list_display = ('id','VERSION', 'HOST_NAME', 'ADMIN_CONSOLE_PORT', 'CATALOG_PORT', 'LDM_Status', 'REGION', 'USERNAME', 'PASSWORD', 'SECURITY_DOMAIN')

class ResourceView(admin.ModelAdmin):
    list_display = ('id','Resource_Name', 'Owner', 'Config', 'Resource_Type', 'ins', 'createdTime','modifiedTime','MarkForDeletion','Refresh_Number')

class ResourceTypeView(admin.ModelAdmin):
    list_display = ('id','resource_type', 'provider_id')


class SearchCountView(admin.ModelAdmin):
    list_display = ('id','search_count')

class ApplicationView(admin.ModelAdmin):
    list_display = ('id','user','apps')

admin.site.register(Instance,InstanceView)

admin.site.register(Resource_Type,ResourceTypeView)

admin.site.register(Resource,ResourceView)

admin.site.register(Search_count,SearchCountView)

admin.site.register(application,ApplicationView)

