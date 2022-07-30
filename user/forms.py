from django import forms
from dashboard.models import *
from .models import Customer
from django.contrib.auth.models import User


class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Customer
        fields = ['full_name','address','username', 'email','password'   ]

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            
            
        }

    def clean_username(self):
        uname = self.cleaned_data.get('username')
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError('Customer with this username already exist')
        return uname 

    def clean_email(self):
        mail = self.cleaned_data.get('email')
        if User.objects.filter(email=mail).exists():
            raise forms.ValidationError('Email already exist')
        return mail

class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
