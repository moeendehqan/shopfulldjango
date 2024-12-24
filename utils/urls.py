from django.urls import path
from utils.views import health_check

urlpatterns = [
    # ... مسیرهای دیگر ...
    path('health/', health_check, name='health_check'),
] 