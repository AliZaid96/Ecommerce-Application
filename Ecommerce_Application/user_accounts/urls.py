from os import name
from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from . import views

urlpatterns = [
    path("register",views.customerRegistration.as_view(), name='register'),
    path('login', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

]
