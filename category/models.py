from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.CharField(max_length=250,null=True,blank=True)
    image = models.ImageField(upload_to='images/')
    status = models.BooleanField(default=True)
    parent = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE)
    description = models.TextField(max_length=500,null=True,blank=True)
    summary = models.TextField(max_length=250,null=True,blank=True)
    keywords = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def save(self, *args, **kwargs):
        if not self.slug:
            slug = str(self.name)
            for char in ['?','!','@','#','$','%','&','*']:
                slug = slug.replace(char, '')
            self.slug = slug.lower().replace(' ', '_')
            
            counter = 1
            original_slug = self.slug
            while Category.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
                
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

