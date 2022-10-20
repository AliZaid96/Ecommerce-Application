from os import name
from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import (
    LoginForm, 
    MyPasswordResetForm,
    MySetPasswordForm,
    MyPasswordChangeForm,
)
from . import views

urlpatterns = [
    path("register", views.customerRegistration.as_view(), name='register'),
    path('login', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html', form_class=MyPasswordResetForm), 
        name='password_reset'
    ),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), 
        name='password_reset_done'
    ),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html', 
        form_class=MySetPasswordForm), 
        name='password_reset_confirm'
    ),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'), 
        name='password_reset_complete'
    ),
    
    path("profile/", views.profile, name="profile"),
    path("update-profile/", views.UpdateProfile.as_view(), name="update-profile"),
    path("address-book", views.addressBook.as_view(), name="address_book"),
    path("delete-address/<int:pk>", views.DeleteAddress.as_view(), name="delete-address"),
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='passwordchange.html', 
        form_class=MyPasswordChangeForm, 
        success_url='accounts/password-changed/'), 
        name='passwordchange'
    ),
    path('password-changed/', auth_views.PasswordChangeDoneView.as_view(
        template_name='password_reset_complete.html'), 
        name='passwordchangedone'
    ),

]
