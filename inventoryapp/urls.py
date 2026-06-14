from django.urls import path
from.import views
urlpatterns = [
    path('categories/',views.CategoryListCreateView.as_view()),
    path('categories/<int:pk>/',views.CategoryDetailsView.as_view()),
    path('suppliers/',views.SupplierListCreateView.as_view()),
    path('suppliers/<int:pk>/',views.SupplierDetailView.as_view()),

    path('products/',views.ProductListCreateView.as_view()),
    path('products/<int:pk>/',views.ProductDetailView.as_view()),

    path('customers/',views.CustomerListCreateView.as_view(),name='customer-list'),
    path('orders/',views.OrderListCreateView.as_view(),name='order-list'),

    path('order-items/',views.OrderItemListCreateView.as_view(),name='order-item-list'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('low-stock/',views.LowStockProductListView.as_view(),name='low-stock-products'),
    path('dashboard/',views.DashboardView.as_view(),name='dashboard'),
]
