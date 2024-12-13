from django.db import models
from django.conf import settings
from product.models import Product

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address = models.TextField()
    postal_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=0)
    paid = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return f'Order {self.id}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.id)
