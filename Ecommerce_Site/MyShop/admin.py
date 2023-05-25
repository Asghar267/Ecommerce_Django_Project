from django.contrib import admin
from .models import Product, Order,  Customer, Cart, Payment, Shipping_Address, Category,User
# from django.contrib.auth.models import User


# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'product_category','quantity', 'price')


admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id',  'name')


admin.site.register(Category, CategoryAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'date_added')


admin.site.register(Cart, CartAdmin)


class Shipping_AddressAdmin(admin.ModelAdmin):
    list_display = ('customer',  'shipping_address',
                    'shipping_country', 'order_date', 'shipping_zip_code')


admin.site.register(Shipping_Address, Shipping_AddressAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'username',
                    'email', 'password', 'address')


admin.site.register(Customer, CustomerAdmin)


# class UserAdmin(admin.ModelAdmin):
#     list_display = ('USERNAME', 'EMAIL ADDRESS',
#                     'FIRST NAME', 'STAFF STATUS', 'PASSWORD')

# admin.site.register(User, UserAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total_price', 'status',
                    'quantity', 'order_date', 'shipping', 'orderitem')
    list_filter = ('status', 'order_date')
    search_fields = ('customer__username', 'shipping__address')


admin.site.register(Order, OrderAdmin)

admin.site.register(Payment)
