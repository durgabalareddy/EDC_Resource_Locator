from django.db import models

from ResourceLocator.models import *

class ManageInstance(models.Model):
    startCMD = models.CharField(max_length=30)
    stopCMD = models.CharField(max_length=30)
    ins = models.ForeignKey(Instance,on_delete=CASCADE)
