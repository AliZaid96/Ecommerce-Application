from os import name
from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home.as_view(), name='home'),
    path('category/<int:id>', views.Category.as_view(), name='category_products'),
    path('product/<int:id>/', views.product_detail, name="product"),

    path('cart/', views.CartView.as_view(), name="cart"),
    path('create-cart/', views.CreateCart.as_view(), name='create_cart'),
    path("add-to-cart/", views.AddToCart, name="addToCart"),

    path("my-orders", views.myOrders, name="my_orders"),
    path("my-orders/<int:id>", views.orderDetail, name='order_detail'),
    path("checkout/", views.checkout, name="checkout"),
    path("place-order/", views.placeOrder, name="placeOrder"),
]
