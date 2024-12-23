#!/bin/bash

# خروجی خطاها را نشان بده
set -e

# Load environment variables
set -a
source .env
set +a

# چاپ اطلاعات اتصال
echo "اطلاعات اتصال به دیتابیس:"
echo "میزبان: $DB_HOST"
echo "کاربر: $DB_USER"
echo "نام دیتابیس: $DB_NAME"

# تلاش برای اتصال و چک کردن
echo "تلاش برای اتصال به دیتابیس..."
PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d postgres -c "SELECT 1" || {
    echo "خطا در اتصال به سرور دیتابیس"
    exit 1
}

# ساخت دیتابیس اگر وجود نداشته باشد
echo "چک کردن وضعیت دیتابیس..."
PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d postgres -c "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || {
    echo "دیتابیس وجود ندارد. در حال ساخت..."
    PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d postgres -c "CREATE DATABASE \"$DB_NAME\""
}

# Generate migrations for all apps
echo "تولید میگریشن‌های جدید..."
python manage.py makemigrations

# Run Django migrations with verbose output
echo "اجرای میگریشن‌ها..."
python manage.py migrate --verbosity 2

# Start the Django application
echo "راه‌اندازی سرور Django..."
exec python manage.py runserver 0.0.0.0:8000