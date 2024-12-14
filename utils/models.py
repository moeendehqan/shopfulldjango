from django.db import models
from django.utils import timezone

class EmailLog(models.Model):
    STATUSES = [
        ('success', 'موفق'),
        ('failed', 'ناموفق'),
    ]

    subject = models.CharField(max_length=255, verbose_name='موضوع')
    sender = models.EmailField(verbose_name='فرستنده')
    recipient = models.EmailField(verbose_name='گیرنده')
    message = models.TextField(verbose_name='متن پیام', blank=True, null=True)
    html_message = models.TextField(verbose_name='متن HTML', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUSES, verbose_name='وضعیت')
    error_message = models.TextField(verbose_name='پیام خطا', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name='زمان ارسال')
    
    class Meta:
        verbose_name = 'گزارش ایمیل'
        verbose_name_plural = 'گزارش‌های ایمیل'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} - {self.recipient} ({self.status})" 