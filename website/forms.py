from django import forms
from dashboard.models import Order
from website.models import *


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields ="__all__"

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['ordered_by', 'location', 'mobile', 'email']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name','review','rate']
