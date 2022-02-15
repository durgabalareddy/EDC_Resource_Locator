from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    HowHelped = models.TextField(max_length=700)
    WhatImproved = models.TextField(max_length=700)

class user(models.Model):
    FullName = models.CharField(max_length=50)
    email = models.EmailField()
    region = models.CharField(max_length=10)