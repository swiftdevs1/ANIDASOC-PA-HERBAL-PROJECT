from django.urls import path
from . import views
from django.urls import reverse_lazy, reverse
from django.contrib.auth import views as auth_views


urlpatterns = [
path("", views.index, name="dashboard-index"),
path("product", views.product, name="dashboard-product"),
path("post", views.post, name="dashboard-post"),
path("testimony", views.testimony, name="testimony"),
path("about_us", views.about_us, name="about_us"),
path("order", views.order, name="dashboard-order"),
path("user", views.user, name="dashboard-user"),
path("message", views.message, name="dashboard-message"),
path("del_message/<int:pk>/", views.del_message, name="del_message"),
path("edit_about/<int:pk>/", views.edit_about, name="edit_about"),
path("profile_detail/<int:pk>/", views.profile_detail, name="dashboard-profile_detail"),
path("category", views.category, name="dashboard-category"),
path("product/edit/<int:pk>/", views.edit_product, name="dashboard-edit-product"),
path("product/delete/<int:pk>/", views.delete_product, name="dashboard-delete-product"),
#path("subscriber", views.subscriber, name="dashboard-subscriber"),
path("new-orders", views.new_orders, name="dashboard-new-orders"),
path("admin_login", views.admin_login, name="admin_login"),
path("logout", views.log_out, name="logout"),
path("success", views.success, name="success"),
path('order-detail/<int:pk>/', views.AdminOrderDetailView.as_view(), name='dashboard-order-detail'),
path('change-order-status/<int:pk>/', views.OrderStatusChangeView.as_view(), name='change-order-status'),
path('change-password/', auth_views.PasswordChangeView.as_view(template_name='dashboard/password_change.html',success_url=reverse_lazy('success')),name='change-password'),
    


]