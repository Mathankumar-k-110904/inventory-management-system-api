from django.db import models

class Category(models.Model):
    CATEGORY_TYPES = [
        ('ELECTRONICS','Electronics'),
        ('FURNITURE','Furniture'),
        ('FOOD','Food'),
        ('STATIONERY','Stationery')
    ]
    name =  models.CharField(max_length=100)
    description = models.TextField()
    category_type = models.CharField(max_length=20,choices=CATEGORY_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class Supplier(models.Model):    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,
                                 related_name='products')
    supplier = models.ForeignKey(Supplier,on_delete=models.SET_NULL,null=True,blank=True,related_name='products'
)
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50,unique=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    minimum_stock = models.PositiveIntegerField(default=10)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Order(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    order_date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Order {self.id}"

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def save(self, *args, **kwargs):

        # if self.quantity > self.product.stock_quantity:
        #     raise ValueError("Not enough stock available.")

        self.subtotal = self.quantity * self.price

        super().save(*args, **kwargs)

        self.product.stock_quantity -= self.quantity
        self.product.save()

        total = sum(
            item.subtotal
            for item in self.order.items.all())
        self.order.total_amount = total
        self.order.save()