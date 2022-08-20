from django import forms
from dashboard.models import Order
from website.models import Blog, Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields ="__all__"

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['ordered_by', 'shipping_address', 'mobile', 'email']
