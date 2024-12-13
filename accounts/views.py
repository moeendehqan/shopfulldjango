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
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'رمزهای عبور مطابقت ندارند.')
            return render(request, self.template_name, self.get_context_data())
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'این ایمیل قبلاً ثبت شده است.')
            return render(request, self.template_name, self.get_context_data())
            
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password1
        )
        login(request, user)
        messages.success(request, 'ثبت نام با موفقیت انجام شد.')
        return redirect('home')

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
