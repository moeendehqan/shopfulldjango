from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'phone_number')
    search_fields = ('email', 'username', 'phone_number')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    ordering = ('email',)
