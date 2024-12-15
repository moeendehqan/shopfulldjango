from typing import Iterable
from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Setting(models.Model):
    title = models.CharField(max_length=150)
    shop_name = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='logos/')
    favicon = models.ImageField(upload_to='logos/')
    address = models.CharField(max_length=150,null=True,blank=True)
    phone = models.CharField(max_length=150,null=True,blank=True)
    email = models.CharField(max_length=150,null=True,blank=True)
    facebook = models.CharField(max_length=150,null=True,blank=True)
    instagram = models.CharField(max_length=150,null=True,blank=True)
    twitter = models.CharField(max_length=150,null=True,blank=True)
    aboutus = models.TextField(max_length=500,null=True,blank=True)
    contact = models.TextField(max_length=500,null=True,blank=True)
    description = models.TextField(max_length=500,null=True,blank=True)
    keywords = models.CharField(max_length=255,null=True,blank=True)
    author = models.CharField(max_length=50,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk and Setting.objects.exists():
            raise ValidationError('There can be only one Setting instance')
        return super(Setting, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Slider(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='sliders/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
