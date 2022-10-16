from os import name
from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home.as_view(), name='home'),
    path('category/<int:id>', views.Category.as_view(), name='category_products'),
    path('product/<int:id>/', views.product_detail, name="product"),
]
