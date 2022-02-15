from django.contrib import admin

from .models import *


class FeedbackView(admin.ModelAdmin):
    list_display = ('id','user', 'HowHelped', 'WhatImproved')

class userView(admin.ModelAdmin):
    list_display = ('id','FullName', 'email', 'region')

admin.site.register(Feedback,FeedbackView)
admin.site.register(user,userView)