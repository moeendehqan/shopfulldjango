from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('categories/', include('category.urls')),
    path('products/', include('product.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('', include('accounts.urls')),
    path('', include('utils.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
