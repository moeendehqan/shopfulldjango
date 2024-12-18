from django import forms
from .models import User
from django.core.validators import RegexValidator

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        label='نام',
        max_length=30,
        validators=[
            RegexValidator(
                regex=r'^[\u0600-\u06FF\s]+$', 
                message='لطفاً فقط از حروف فارسی استفاده کنید'
            )
        ],
        widget=forms.TextInput(attrs={
            'placeholder': 'نام خود را وارد کنید',
            'class': 'appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 bg-gray-50 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:bg-white focus:z-10 sm:text-sm'
        })
    )

    last_name = forms.CharField(
        label='نام خانوادگی',
        max_length=30,
        validators=[
            RegexValidator(
                regex=r'^[\u0600-\u06FF\s]+$', 
                message='لطفاً فقط از حروف فارسی استفاده کنید'
            )
        ],
        widget=forms.TextInput(attrs={
            'placeholder': 'نام خانوادگی خود را وارد کنید',
            'class': 'appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 bg-gray-50 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:bg-white focus:z-10 sm:text-sm'
        })
    )

    phone_number = forms.CharField(
        label='شماره تلفن همراه',
        validators=[
            RegexValidator(
                regex=r'^09\d{9}$', 
                message='لطفاً شماره تلفن همراه را با فرمت صحیح وارد کنید (مثال: 09123456789)'
            )
        ],
        widget=forms.TextInput(attrs={
            'placeholder': 'شماره تلفن همراه خود را وارد کنید',
            'class': 'appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 bg-gray-50 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:bg-white focus:z-10 sm:text-sm'
        })
    )

    postal_code = forms.CharField(
        label='کد پستی',
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$', 
                message='کد پستی باید 10 رقم باشد'
            )
        ],
        widget=forms.TextInput(attrs={
            'placeholder': 'کد پستی خود را وارد کنید',
            'class': 'appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 bg-gray-50 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:bg-white focus:z-10 sm:text-sm'
        })
    )

    address = forms.CharField(
        label='آدرس',
        max_length=300,
        widget=forms.Textarea(attrs={
            'placeholder': 'آدرس کامل خود را وارد کنید',
            'class': 'appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 bg-gray-50 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:bg-white focus:z-10 sm:text-sm',
            'rows': 3
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'postal_code', 'address']

    def __init__(self, *args, **kwargs):
        # اگر یک نمونه کاربر به فرم پاس داده شده باشد
        if 'instance' in kwargs:
            user = kwargs['instance']
            # مقادیر پیش‌فرض را از مدل کاربر بخوان
            initial = kwargs.get('initial', {})
            initial['first_name'] = user.first_name
            initial['last_name'] = user.last_name
            initial['phone_number'] = user.phone_number
            initial['postal_code'] = user.postal_code
            initial['address'] = user.address
            
            # آپدیت کردن initial با مقادیر پیش‌فرض
            kwargs['initial'] = initial

        # فراخوانی متد اصلی __init__
        super().__init__(*args, **kwargs)