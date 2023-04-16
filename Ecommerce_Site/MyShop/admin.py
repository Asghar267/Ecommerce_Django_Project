from django.contrib import admin
from .models import Product, Order, ShippingAddress, Customer, Cart, Payment

# Register your models here.

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(ShippingAddress)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(Payment)