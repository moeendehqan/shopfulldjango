import os
from django.core.mail import EmailMessage
from django.conf import settings

class EmailService:
    @staticmethod
    def send_email(
        subject: str, 
        message: str, 
        recipient_list: list[str], 
        from_email: str = None,
        html_message: str = None,
        attachments: list = None
    ):
        """
        ارسال ایمیل با استفاده از تنظیمات SMTP
        
        :param subject: موضوع ایمیل
        :param message: متن ایمیل
        :param recipient_list: لیست گیرندگان
        :param from_email: ایمیل فرستنده (اختیاری)
        :param html_message: متن HTML ایمیل (اختیاری)
        :param attachments: پیوست‌های ایمیل (اختیاری)
        :return: وضعیت ارسال ایمیل
        """
        try:
            # تنظیمات SMTP از محیط
            email = EmailMessage(
                subject=subject,
                body=message or html_message,
                from_email=from_email or settings.DEFAULT_FROM_EMAIL,
                to=recipient_list
            )
            
            # اگر HTML ایمیل است
            if html_message:
                email.content_subtype = 'html'
            
            # افزودن پیوست‌ها
            if attachments:
                for attachment in attachments:
                    email.attach_file(attachment)
            
            # ارسال ایمیل
            result = email.send()
            return {
                'success': True,
                'message': 'ایمیل با موفقیت ارسال شد',
                'recipients': recipient_list
            }
        
        except Exception as e:
            return {
                'success': False, 
                'message': str(e),
                'error': e
            }

# تنظیمات SMTP در settings.py
SMTP_SETTINGS = {
    'EMAIL_HOST': os.getenv('SMTP_HOST', 'smtp.c1.liara.email'),
    'EMAIL_PORT': int(os.getenv('SMTP_PORT', 465)),
    'EMAIL_HOST_USER': os.getenv('SMTP_USER', 'determined_blackburn_m0gpqt'),
    'EMAIL_HOST_PASSWORD': os.getenv('SMTP_PASSWORD', 'dd4c5284-90db-4ada-90c4-e8c2768efe35'),
    'EMAIL_USE_SSL': True,
} 