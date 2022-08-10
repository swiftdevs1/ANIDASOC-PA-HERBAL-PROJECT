from django.urls import path
from . import views

urlpatterns = [
path('register', views.CustomerRegistrationView.as_view(), name='user-registration'),
path('logout', views.CustomerLogoutView.as_view(), name='user-logout'),
path('', views.CustomerLoginView.as_view(), name='user-login'),
path("user-profile",views.profile, name="user-profile"),
    

]