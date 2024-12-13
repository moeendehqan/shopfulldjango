from django.contrib import admin
from .models import Setting, Slider
    
# Register your models here.
admin.site.register(Setting)
@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title']
    ordering = ['-created_at']

