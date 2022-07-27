from django.urls import path
from . import views

urlpatterns = [
path("", views.index, name="dashboard-index"),
path("product", views.product, name="dashboard-product"),
path("order", views.order, name="dashboard-order"),
path("user", views.user, name="dashboard-user"),
path("profile", views.profile, name="dashboard-profile"),
path("category", views.category, name="dashboard-category"),
path("product/edit/<int:pk>/", views.edit_product, name="dashboard-edit-product"),
path("product/delete/<int:pk>/", views.delete_product, name="dashboard-delete-product"),
path("subscriber", views.subscriber, name="dashboard-subscriber"),
path("new-orders", views.new_orders, name="dashboard-new-orders"),
path('order-detail/<int:pk>/', views.AdminOrderDetailView.as_view(), name='dashboard-order-detail'),
path('change-order-status/<int:pk>/', views.OrderStatusChangeView.as_view(), name='change-order-status'),

]