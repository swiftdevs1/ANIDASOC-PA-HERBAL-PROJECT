from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
path('register', views.register, name='register'),
path('', views.sign_in, name='user-login'),
path('logout', views.sign_out, name='user-logout'),
path('profile', views.profile, name='profile'),
path('profile_update', views.profile_update, name='profile_update'),
path('user_home', views.user_home, name='user_home'),
path('setting', views.setting, name='setting'),
path ('profile/order-<int:pk>/', views.CustomerOrderDetail.as_view(), name='customerorderdetail'),

# ******************* RESET PASSWORD VIEW *****************************
path('password_reset', auth_views.PasswordResetView.as_view(
    template_name='user/reset_password.html'), name='password_reset'),
path('password_reset_done', auth_views.PasswordResetDoneView.as_view(
    template_name='user/reset_password_done.html'), name='password_reset_done'),
path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    template_name='user/reset_password_confirm.html'), name='password_reset_confirm'),
path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(
    template_name='user/reset_password_complete.html'), name='password_reset_complete'),


]