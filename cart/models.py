from django.db import models
from django.contrib.auth.models import User
from product.models import Product
import uuid
from django.conf import settings

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart {self.id}"
    
    class Meta:
        indexes = [
            models.Index(fields=['session_id']),
            models.Index(fields=['user']),
        ]

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ForeignKey('product.Variation', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('cart', 'variation')
        indexes = [
            models.Index(fields=['cart', 'variation']),
        ]

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.variation})"

    @property
    def total_price(self):
        return self.quantity * self.variation.price_after_discount if self.variation.price_after_discount else self.quantity * self.variation.price
