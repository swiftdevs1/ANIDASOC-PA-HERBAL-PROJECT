from django import forms
from .models import Product,Category
from website.models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title','slug','category','image','marked_price','selling_price','status','description']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = "__all__"

class TestimonyForm(forms.ModelForm):
    class Meta:
        model = Testimony
        fields = "__all__"

class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = "__all__"
