from django.contrib import admin
from .models import Category
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug','image','status']
    list_filter = ['status']
    list_editable = ['status']
    search_fields = ['name','slug']
    list_per_page = 10
    list_display_links = ['name']
    list_max_show_all = 100
    list_select_related = True
    list_select_related = True

