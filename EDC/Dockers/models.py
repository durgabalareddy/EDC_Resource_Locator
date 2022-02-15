from django.db import models

class dockers(models.Model):
    CaseNo = models.CharField(max_length=50)
    Host = models.CharField(max_length=100)
    Version = models.CharField(max_length=50)
    expiryDate = models.CharField(max_length=50)
    pVersion = models.CharField(max_length=50)
    createdDate = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    email = models.EmailField()
    Visibilty = models.BooleanField(default=True)
    Note = models.TextField(max_length=200)
    refreshNumber = models.BigIntegerField(default=0)

class user(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField()
    region = models.CharField(max_length=10)