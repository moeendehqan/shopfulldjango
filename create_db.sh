#!/bin/bash

# خروجی خطاها را نشان بده
set -e

# Load environment variables
set -a
source .env
set +a

# چاپ اطلاعات اتصال
echo "اطلاعات اتصال به دیتابیس 22:"
echo "میزبان: $DB_HOST"
echo "کاربر: $DB_USER"
echo "نام دیتابیس: $DB_NAME"

# تلاش برای اتصال و چک کردن

# Generate migrations for all apps
echo "تولید میگریشن‌های جدید..."
python manage.py makemigrations accounts
python manage.py makemigrations cart
python manage.py makemigrations category
python manage.py makemigrations home
python manage.py makemigrations order
python manage.py makemigrations product
python manage.py makemigrations utils
python manage.py makemigrations


python manage.py migrate

# ایجاد کاربر ادمین
echo "ایجاد کاربر ادمین..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'RoundShop2024!')
"

