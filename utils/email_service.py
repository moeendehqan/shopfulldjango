from home.models import Setting
from .models import EmailLog
import os
import smtplib
import ssl
from django.core.mail import EmailMessage
from email.mime.text import MIMEText
from email.header import Header

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
            # دریافت تنظیمات از مدل Setting
            setting = Setting.objects.first()
            
            # تعیین پورت و نوع اتصال
            smtp_host = setting.smtpserver
            smtp_username = setting.smtpusername
            smtp_password = setting.smtppassword
            
            # اولویت با SMTPS
            if setting.smtpsport:
                smtp_port = int(setting.smtpsport)
                use_ssl = True
            else:
                smtp_port = int(setting.smtpport or 587)
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
                msg['From'] = from_email or setting.smtpemail
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
                    sender=from_email or setting.smtpemail,
                    recipient=recipient,
                    message=message,
                    html_message=html_message,
                    status='success'
                )
            
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
                    sender=from_email or setting.smtpemail,
                    recipient=recipient,
                    message=message,
                    html_message=html_message,
                    status='failed',
                    error_message=str(e)
                )
            
            # چاپ جزئیات خطا برای دیباگ
            print(f"SMTP Error Details:")
            print(f"Host: {setting.smtpserver}")
            print(f"Port SMTPS: {setting.smtpsport}")
            print(f"Port SMTP: {setting.smtpport}")
            print(f"Username: {setting.smtpusername}")
            print(f"Full Error: {str(e)}")
            
            return {
                'success': False, 
                'message': str(e),
                'error': e
            }
