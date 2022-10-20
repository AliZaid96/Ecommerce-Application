from os import name
from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home.as_view(), name='home'),
    path('category/<int:id>', views.Category.as_view(), name='category_products'),
    path('product/<int:id>/', views.product_detail, name="product"),

    path("my-orders", views.myOrders, name="my_orders"),
    path("order-details/<int:id>", views.orderDetail, name='order_detail'),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("confirm-order/<str:session_ID>", views.ConfirmOrderView.as_view(), name="confirm-order"),
    path("place-order/<str:session_ID>", views.placeOrder, name="placeOrder"),
    path('cancel-order/<int:pk>', views.CancelOrder, name='canceled'),

    path('webhook/stripe/', views.stripeWebhookView, name='stripe-webhook'),

    path('newsletter-subscription', views.NewsletterSubscriptionView, name='subscribe-to-newsletter'),
    path('contact-us', views.ContactUSView.as_view(), name='contact-us'),
    # View to sync products with stripe store
    path('sync-with-stripe', views.SyncDataWithStripe, name='sync-with-stripe'),
]
