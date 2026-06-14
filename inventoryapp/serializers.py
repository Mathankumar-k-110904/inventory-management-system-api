from rest_framework import serializers
from .models import Category,Supplier,Product,Customer,Order,OrderItem
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_price(self,value):
        if value<=0:
            raise serializers.ValidationError(
                "price must be greater than zero"
            )
        return value
            
    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError(
            "Stock quantity cannot be negative."
            )
        return value

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
    
    def validate(self, data):
        product = data['product']
        quantity = data['quantity']

        if quantity > product.stock_quantity:
            raise serializers.ValidationError(
                "Not enough stock available."
            )

        return data



class OrderItemNestedSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source='product.name',
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            'product_name',
            'quantity',
            'price',
            'subtotal'
        ]
class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemNestedSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Order
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user