from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_id', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'session_id')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('cart__id', 'product__name')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at')
