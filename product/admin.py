from django.contrib import admin
from .models import Product,Variation,Color,Size,Image

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','slug','image','published','created_at','updated_at']
    list_filter = ['published','created_at','updated_at']
    search_fields = ['name','slug']
    list_per_page = 20

@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'price', 'price_after_discount', 'stock', 'color', 'size', 'published', 'created_at', 'updated_at']
    list_filter = ['published','created_at','updated_at']
    search_fields = ['product']
    list_per_page = 20
    

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name','code']
    list_filter = ['name','code']
    search_fields = ['name','code']
    list_per_page = 20

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name','code']
    list_filter = ['name','code']
    search_fields = ['name','code']
    list_per_page = 20

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['alt','image']
    list_filter = ['alt','image']
    search_fields = ['alt','image']
    list_per_page = 20

