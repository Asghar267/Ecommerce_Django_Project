from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Customer(models.Model):
    id = models.AutoField(primary_key=True,)
    full_name = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    # password2 = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    zip_code = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.full_name


class Product(models.Model):

    lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=150)
    # product_category = models.CharField(max_length=50)
    product_category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=1)
    description = models.TextField(default=lorem)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(
        upload_to='product_images/', blank=True, null=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.product_name


class Shipping_Address(models.Model):

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    shipping_address = models.CharField(max_length=100, null=True)
    shipping_city = models.CharField(max_length=50, null=True)
    shipping_state = models.CharField(max_length=50, null=True)
    shipping_country = models.CharField(max_length=50, null=True)
    shipping_zip_code = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f"{self.shipping_address} {self.shipping_state}, {self.shipping_country}"
        # return self.shipping_address+self.self.shipping_state+self.shipping_country


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s cart: {self.product.product_name} x {self.quantity}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    orderitem = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    shipping = models.ForeignKey(Shipping_Address, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Pending")
    order_date = models.DateTimeField(auto_now_add=True, null=True)
    # shipping_address = models.CharField(max_length=100)
    # shipping_address = models.CharField(max_length=100)
    # shipping_city = models.CharField(max_length=50)
    # shipping_state = models.CharField(max_length=50)
    # shipping_country = models.CharField(max_length=50)
    # shipping_zip_code = models.CharField(max_length=10)

    # quantity = int(request.POST[f'product_{product_id}_quantity'])

    # OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)
    def __str__(self):
        return self.customer.first_name


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.pname
