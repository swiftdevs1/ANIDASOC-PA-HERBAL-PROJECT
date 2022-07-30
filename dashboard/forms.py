from django import forms
from .models import Product,Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title','slug','category','image','marked_price','selling_price','status','description']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title','slug','status']
