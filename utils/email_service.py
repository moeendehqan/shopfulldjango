from home.models import Setting
from .models import EmailLog
import os
import smtplib
import ssl
from django.core.mail import EmailMessage
from email.mime.text import MIMEText
from email.header import Header
from django.conf import settings
class EmailService:
    @staticmethod
    def send_email(
        subject: str, 
        message: str = None, 
        recipient_list: list[str] = None, 
        from_email: str = None,
        html_message: str = None,
        attachments: list = None
    ):
        try:
            
            # تعیین پورت و نوع اتصال
            smtp_host = settings.EMAIL_HOST
            smtp_username = settings.EMAIL_HOST_USER
            smtp_password = settings.EMAIL_HOST_PASSWORD
            
            # اولویت با SMTPS
            if settings.EMAIL_PORT_SMTPS:
                smtp_port = int(settings.EMAIL_PORT_SMTPS)
                use_ssl = True
            else:
                smtp_port = int(settings.EMAIL_PORT_SMTP or 587)
                use_ssl = False
            
            # ایجاد کانتکست SSL
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            # انتخاب متد اتصال
            if use_ssl:
                server = smtplib.SMTP_SSL(smtp_host, smtp_port, context=context)
            else:
                server = smtplib.SMTP(smtp_host, smtp_port)
                server.starttls(context=context)
            
            try:
                # ورود به سرور
                server.login(smtp_username, smtp_password)
                
                # ساخت ایمیل با کدگذاری UTF-8
                msg = MIMEText(html_message or message, 'html', 'utf-8')
                msg['Subject'] = Header(subject, 'utf-8')
                msg['From'] = from_email or settings.DEFAULT_FROM_EMAIL
                msg['To'] = ', '.join(recipient_list)
                
                # ارسال ایمیل
                server.sendmail(
                    from_addr=msg['From'], 
                    to_addrs=recipient_list, 
                    msg=msg.as_string()
                )
            finally:
                # بستن اتصال
                server.quit()
            
            # ذخیره گزارش ایمیل موفق
            for recipient in recipient_list:
                EmailLog.objects.create(
                    subject=subject,
                    sender=from_email or settings.DEFAULT_FROM_EMAIL,
                    recipient=recipient,
                    message=message,
                    html_message=html_message,
                    status='success'
                )
            
            # چاپ اطلاعات دقیق SMTP برای دیباگ
            print("SMTP Debug Info:")
            print(f"Host: {smtp_host}")
            print(f"Port: {smtp_port}")
            print(f"Username: {smtp_username}")
            print(f"SSL/TLS: {use_ssl}")
            
            return {
                'success': True,
                'message': 'ایمیل با موفقیت ارسال شد',
                'recipients': recipient_list
            }
        
        except Exception as e:
            # ذخیره گزارش ایمیل ناموفق
            for recipient in recipient_list or []:
                EmailLog.objects.create(
                    subject=subject,
                    sender=from_email or settings.DEFAULT_FROM_EMAIL,
                    recipient=recipient,
                    message=message,
                    html_message=html_message,
                    status='failed',
                    error_message=str(e)
                )
            
            # چاپ جزئیات خطا برای دیباگ
            print(f"SMTP Error Details:")
            print(f"Host: {settings.EMAIL_HOST}")
            print(f"Port SMTPS: {settings.EMAIL_PORT_SMTPS}")
            print(f"Port SMTP: {settings.EMAIL_PORT_SMTP}")
            print(f"Username: {settings.EMAIL_HOST_USER}")
            print(f"Full Error: {str(e)}")
            
            return {
                'success': False, 
                'message': str(e),
                'error': e
            }
