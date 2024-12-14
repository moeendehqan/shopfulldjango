from django.contrib import admin
from .models import EmailLog

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'recipient', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('subject', 'sender', 'recipient') 