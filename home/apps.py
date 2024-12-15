from django.apps import AppConfig
from django.db.models.signals import post_migrate

def configure_email_settings(sender, **kwargs):
    from django.conf import settings
    try:
        from home.models import Setting
        setting = Setting.objects.first()
        if setting:
            settings.DEFAULT_FROM_EMAIL = setting.smtpemail
            settings.EMAIL_HOST = setting.smtpserver
            settings.EMAIL_PORT = int(setting.smtpport)
            settings.EMAIL_HOST_USER = setting.smtpusername
            settings.EMAIL_HOST_PASSWORD = setting.smtppassword
    except Exception:
        pass

class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self):
        post_migrate.connect(configure_email_settings, sender=self)
