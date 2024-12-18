from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    phone_number = models.CharField(_('شماره همراه'), max_length=11, unique=True, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(
        unique=True,
        verbose_name='email address',
        max_length=255,
    )
    first_name = models.CharField(_('نام'), max_length=50, blank=True, null=True)
    last_name = models.CharField(_('نام خانوادگی'), max_length=50, blank=True, null=True)
    birth_date = models.DateField(_('تاریخ تولد'), null=True, blank=True)
    address = models.TextField(_('آدرس'), blank=True, null=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email
