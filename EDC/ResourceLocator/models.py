from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from ckeditor.fields import RichTextField


class Resource_Type(models.Model):
    resource_type = models.CharField(max_length=100)
    provider_id = models.CharField(max_length=100)
    MITI_Scanner = models.BooleanField(default=False)
    #Scanner_url = models.TextField(max_length=500)
    Quick_Links = RichTextField(blank=True,null=True)



    def __str__(self):
        return f'{self.resource_type}'

class Instance(models.Model):
    HOST_NAME = models.CharField(max_length=50)
    VERSION = models.CharField(max_length=50)
    ADMIN_CONSOLE_PORT = models.IntegerField()
    CATALOG_PORT = models.IntegerField()
    LDM_Status = models.BooleanField()
    REGION = models.CharField(max_length=10)
    USERNAME = models.CharField(max_length=20)
    PASSWORD = models.CharField(max_length=30)
    SECURITY_DOMAIN = models.CharField(max_length=20)
    

    

    def __str__(self):
        return f'{self.VERSION}'
    
class Resource(models.Model):
    Resource_Name = models.CharField(max_length=200)
    Owner = models.CharField(max_length=30)
    Config = models.CharField(max_length=100)
    Resource_Type = models.ForeignKey(Resource_Type,on_delete=CASCADE)
    ins = models.ForeignKey(Instance,on_delete=CASCADE)
    createdTime = models.CharField(max_length=20)
    modifiedTime= models.CharField(max_length=20)
    MarkForDeletion = models.BooleanField(default=False)
    Refresh_Number = models.BigIntegerField(default=0)


    def __str__(self):
        return f'{self.Resource_Name}'


class Search_count(models.Model):
    search_count = models.BigIntegerField()

    def __str__(self):
        return f'{self.search_count}'

class application(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='applicationList',null=True)
    #application_list = models.CharField(max_length=20,default='ResourceLocator')
    apps = ArrayField(models.CharField(max_length=90), blank=True)
