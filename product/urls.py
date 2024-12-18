from django.urls import path, re_path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    re_path(r'^(?P<slug>[\w-]+)/$', views.ProductDetailView.as_view(), name='product_detail'),
] 