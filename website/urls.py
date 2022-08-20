from django.urls import path
from . import views

urlpatterns = [
path("", views.home, name="website-home"),
path("blog", views.blog, name="blog"),
path("about", views.about, name="about"),
path("contact", views.contact, name="contact"),
path("send", views.send, name="send"),
path("search", views.search, name="search"),
path("category", views.category, name="website-cat"),
path("collection/<str:slug>", views.collection, name="collection"),
path("product/detail/<int:pk>", views.product_details, name="website-product-detail"),
path("add-to-cart/<int:pro_id>", views.AddToCartView.as_view(), name="website-add-to-cart"),
path('my-cart/', views.MyCartView.as_view(), name='mycart'),
path('manage-cart/<int:cp_id>/', views.ManageCartView.as_view(), name='managecart'),
path('empty-cart/', views.EmptyCartView.as_view(), name='emptycart'),
path('checkout/', views.CheckOutView.as_view(), name='checkout'),

]