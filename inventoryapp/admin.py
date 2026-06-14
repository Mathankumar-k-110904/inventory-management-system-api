from django.contrib import admin
from.models import Category,Supplier,Product,Order,Customer,OrderItem

admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)