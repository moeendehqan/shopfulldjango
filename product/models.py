from typing import Iterable
from django.db import models
from category.models import Category
from accounts.models import User
from django.utils import timezone



class Color(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=150)
    def __str__(self):
        return f'{self.name} - {self.code}'

class Size(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=150)
    def __str__(self):
        return f'{self.name} - {self.code}'

class Image(models.Model):
    alt = models.CharField(max_length=150)
    image = models.ImageField(upload_to='images/')
    def __str__(self):
        return f'{self.alt} - {self.id}'

class Product(models.Model):
    name = models.CharField(max_length=150)
    slug = models.CharField(max_length=250,null=True,blank=True)
    image = models.ImageField(upload_to='images/')
    published = models.BooleanField(default=True)
    description = models.TextField(max_length=500,null=True,blank=True)
    summary = models.TextField(max_length=250,null=True,blank=True)
    keywords = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.slug:
            print('name:',self.name)
            slug = str(self.name).lower()
            print('slug:',slug)
            for char in ['?','!','@','#','$','%','&','*']:
                slug = slug.replace(char, '')
            self.slug = slug.lower().replace(' ', '_')
            counter = 1
            original_slug = self.slug
            while Product.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
                
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.slug}'

class Variation(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    price_after_discount = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    color = models.ForeignKey(Color,on_delete=models.CASCADE,null=True,blank=True)
    size = models.ForeignKey(Size,on_delete=models.CASCADE,null=True,blank=True)
    image = models.ManyToManyField(Image)
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_default = models.BooleanField(default=False)

    def save(self) -> None:
        if self.is_default:
            Variation.objects.filter(product=self.product).update(is_default=False)
        if not Variation.objects.filter(product=self.product, is_default=True).exists():
            self.is_default = True
        return super().save()

    def __str__(self):
        size = self.size.name if self.size else 'اندازه پیش فرض'
        color = self.color.name if self.color else 'رنگ پیش فرض'
        return f'{self.product.name} - {color} - {size} - {self.product.slug}'




class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    comment = models.TextField(max_length=500,null=True,blank=True)
    rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.user.username} - {self.product.name}'