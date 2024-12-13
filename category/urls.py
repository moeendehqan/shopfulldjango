from django.urls import path
from . import views

urlpatterns = [
    path('', views.AllCategoriesView.as_view(), name='categories'),
    path('category/<str:slug>/', views.CategoryView.as_view(), name='category'),
]
