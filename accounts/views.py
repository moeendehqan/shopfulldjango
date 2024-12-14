from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import View
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetConfirmView,
    PasswordChangeView
)
from .models import User
from home.models import Setting
import uuid
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from utils.email_service import EmailService

class LoginView(View):
    template_name = 'accounts/login.html'
    
    def get_context_data(self):
        setting = Setting.objects.first()
        return {
            'description': setting.description,
            'keywords': setting.keywords,
            'author': setting.author,
            'robots': 'index, follow',
            'title': setting.title,
            'logo': setting.logo,
            'favicon': setting.favicon
        }
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name, self.get_context_data())
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'با موفقیت وارد شدید.')
            return redirect('home')
        
        messages.error(request, 'ایمیل یا رمز عبور اشتباه است.')
        return render(request, self.template_name, self.get_context_data())

class RegisterView(View):
    template_name = 'accounts/register.html'
    
    def get_context_data(self):
        setting = Setting.objects.first()
        return {
            'description': setting.description,
            'keywords': setting.keywords,
            'author': setting.author,
            'robots': 'index, follow',
            'title': setting.title,
            'logo': setting.logo,
            'favicon': setting.favicon
        }

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name, self.get_context_data())
    
    def post(self, request):
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # اعتبارسنجی ایمیل
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'ایمیل نامعتبر است.')
            return render(request, self.template_name, self.get_context_data())
        
        # اعتبارسنجی شماره تلفن
        if not phone_number or not phone_number.startswith('09') or len(phone_number) != 11:
            messages.error(request, 'شماره تلفن نامعتبر است.')
            return render(request, self.template_name, self.get_context_data())
        
        if password1 != password2:
            messages.error(request, 'رمزهای عبور مطابقت ندارند.')
            return render(request, self.template_name, self.get_context_data())
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'این ایمیل قبلاً ثبت شده است.')
            return render(request, self.template_name, self.get_context_data())
        
        if User.objects.filter(phone_number=phone_number).exists():
            messages.error(request, 'این شماره تلفن قبلاً ثبت شده است.')
            return render(request, self.template_name, self.get_context_data())
            
        # ایجاد توکن تایید ایمیل
        verification_token = str(uuid.uuid4())
        
        user = User.objects.create_user(
            username=email,
            email=email,
            phone_number=phone_number,
            password=password1,
            is_email_verified=False,
            email_verification_token=verification_token
        )
        
        # ارسال ایمیل تایید
        verification_link = request.build_absolute_uri(
            reverse_lazy('verify_email', kwargs={'token': verification_token})
        )
        
        email_result = EmailService.send_email(
            subject='تایید ایمیل',
            html_message=f'''
            <p>برای تایید ایمیل خود روی لینک زیر کلیک کنید:</p>
            <a href="{verification_link}">تایید ایمیل</a>
            ''',
            recipient_list=[email]
        )
        
        if not email_result['success']:
            # اگر ارسال ایمیل موفق نبود، کاربر را حذف کنیم
            user.delete()
            messages.error(request, 'خطا در ارسال ایمیل تایید. لطفاً مجدداً تلاش کنید.')
            return render(request, self.template_name, self.get_context_data())
        
        messages.success(request, 'ثبت نام با موفقیت انجام شد. لطفاً ایمیل خود را تایید کنید.')
        return redirect('login')

class VerifyEmailView(View):
    def get(self, request, token):
        try:
            user = User.objects.get(email_verification_token=token)
            user.is_email_verified = True
            user.email_verification_token = None
            user.save()
            
            messages.success(request, 'ایمیل شما با موفقیت تایید شد.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'توکن تایید نامعتبر است.')
            return redirect('login')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        setting = Setting.objects.first()
        context.update({
            'description': setting.description,
            'keywords': setting.keywords,
            'author': setting.author,
            'robots': 'index, follow',
            'title': setting.title,
            'logo': setting.logo,
            'favicon': setting.favicon
        })
        return context

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'با موفقیت خارج شدید.')
    return redirect('home')
