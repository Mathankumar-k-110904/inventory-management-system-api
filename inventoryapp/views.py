from django.shortcuts import render
from .models import Category,Supplier,Product,Order,Customer,OrderItem
from .serializers import CategorySerializer,SupplierSerializer,ProductSerializer,CustomerSerializer,OrderSerializer,OrderItemSerializer, RegisterSerializer
from rest_framework.response import Response
from rest_framework import generics,filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAdminOrReadOnly
from django.contrib.auth.models import User
from django.db.models import F
from rest_framework.views import APIView

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class CategoryDetailsView(generics.RetrieveUpdateDestroyAPIView,):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SupplierListCreateView(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]


class SupplierDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['name','sku']
    ordering_fields = ['price',
    'stock_quantity',
    'created_at']

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemListCreateView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class LowStockProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(
            stock_quantity__lt=10
        )
    
class DashboardView(APIView):

    def get(self, request):

        data = {
            "total_products": Product.objects.count(),
            "total_customers": Customer.objects.count(),
            "total_orders": Order.objects.count(),
            "low_stock_products": Product.objects.filter(
                stock_quantity__lt=F('minimum_stock')
            ).count()
        }

        return Response(data)