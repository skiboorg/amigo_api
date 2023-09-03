from django.db import models

class CallbackForm(models.Model):
    phone = models.CharField(max_length=255,blank=True, null=True)
    email = models.CharField(max_length=255,blank=True, null=True)
    userName = models.CharField(max_length=255,blank=True, null=True)
    orderComment = models.TextField(blank=True, null=True)