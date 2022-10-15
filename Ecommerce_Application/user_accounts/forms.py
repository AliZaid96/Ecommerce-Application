from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UsernameField,
    UserCreationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.forms import fields, widgets
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth import password_validation


class LoginForm(AuthenticationForm):
    username = UsernameField(widget = forms.TextInput(
        attrs = {'autofocus':True,
            'class':'form-control'
        }
    ))
    password = forms.CharField(label = _('Password'),
        strip = False,
        widget = forms.PasswordInput(
            attrs = {'autocomplete':'current-password', 'autofocus':True, 'class':'form-control'}
        )
    )

class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label = 'Password',
        widget = forms.PasswordInput(attrs = {'class':'form-control'})
    )
    password2 = forms.CharField(label = 'Confirm Password (again)',
        widget = forms.PasswordInput(attrs = {'class':'form-control'})
    )
    email = forms.CharField(required = True, 
        widget = forms.EmailInput(attrs = {'class':'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'email':'Email',
            'first_name':"First Name",
            'last_name':"Last Name"
        }
        widgets = {
            'username':forms.TextInput(attrs = {'class':'form-control'}),
            'first_name':forms.TextInput(attrs = {'class':'form-control'}),
            'last_name':forms.TextInput(attrs = {'class':'form-control'})
        }

class MyPasswordResetForm(PasswordResetForm):
    email=forms.EmailField(label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(
            attrs={'autocomplete':'email','class':'form-control'}
        )
    )

class MySetPasswordForm(SetPasswordForm):
    new_password1=forms.CharField(label='New Password',
        widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),
        help_text=password_validation.password_validators_help_text_html()
    )
    new_password2=forms.CharField(label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'})
    )

