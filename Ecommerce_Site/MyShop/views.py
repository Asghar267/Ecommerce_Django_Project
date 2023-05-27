from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Customer, Product, Order, Shipping_Address, Payment, Cart, Category
from .forms import CreateUserForm, BulkProductUploadForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random


def search(request):
    search_term = request.GET.get('q')
    print("search_term: ", search_term)
    if not search_term:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(product_name__icontains=search_term)
    return render(request, 'product_list.html', {'products': products, 'search_term': search_term})


def register_user(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        username = request.POST['username']
        first_name = request.POST['full_name']
        email = request.POST['email']
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        print("username:", username)
        print("password1:", password)
        print("confirm_password:", confirm_password)

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register_user')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect(register_user)

        user = User.objects.create_user(
            first_name=first_name, username=username, email=email, password=password)
        user.save()
        messages.success(
            request, "Registration successful. You can now log in.")

        # print("Field Error:", field.name,  field.errors) # debugging
        # print("Form Error:", form.errors)

        redirect('login_user')

    context = {"form": form}
    return render(request, "register.html", context)


def loginUser(request):
    if request.method == "POST":
        username1 = request.POST['username']
        password1 = request.POST['password1']
        user = authenticate(request, username=username1, password=password1)
        if user is not None:
            login(request, user)
            next_param = request.GET.get('next')
            if next_param and next_param != "/signin/":
                print("next_param:", next_param)
                return redirect(next_param)
            else:
                # Replace 'home' with the appropriate URL name for the default page
                return redirect(reverse('product_list'))
        else:
            messages.info(request, "Username or Password is incorrect!")
            return render(request, "login.html")

    return render(request, "login.html")


@login_required(login_url='login_user')
def logoutUser(request):
    logout(request)
    return redirect('login_user')


@login_required(login_url='login_user')
def profileUser(request):
    print('request.user :', request.user)
    print('request.user att :', request.user.is_authenticated)
    user = User.objects.filter(username=request.user)
    order = Order.objects.filter(customer=request.user)
    print(user)
    print("order :", order)
    return render(request, "profile.html", {'user': user, 'order': order})


@login_required(login_url='login_user')
def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    return render(request, 'customer_detail.html', {'customer': customer})


def product_list(request):
    # products = Product.objects.all()
    products = Product.objects.order_by('?')

    categories = Category.objects.all()
    categoryId = request.GET.get("category")
    if categoryId:  # filter products
        category = Category.objects.get(id=categoryId)
        products = Product.objects.filter(product_category=category)
    return render(request, 'product_list.html', {'products': products, 'categories': categories})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})


def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order_items = Order.objects.filter(order=order)
    # order_items = OrderItem.objects.filter(order=order)
    return render(request, 'order_detail.html', {'order': order, 'order_items': order_items})


# session based
def add_to_cart(request, product_id):
    quantity = request.POST['quantity']
    print("Quantity:", quantity)
    product = Product.objects.get(pk=product_id)
    cart_item = {
        'product_id': product_id,
        'quantity': int(quantity),
    }

    if request.session.get('cart'):
        cart = request.session['cart']
        if product_id in cart:
            cart[product_id]['quantity'] += int(quantity)
        else:
            cart[product_id] = cart_item
        request.session.modified = True
    else:
        cart = {
            product_id: cart_item
        }
        request.session['cart'] = cart

    messages.success(request, 'Item added successfully!')
    print(messages)

    return redirect('product_list')


# session  based
def cart(request):
    if request.method == 'POST':
        user_r = request.user
        cart_items = Cart.objects.filter(user=user_r)

        ShippingAddress(request)
        shipping_Address = Shipping_Address.objects.filter(customer=user_r)[0]

        # Create a new Cart object for each item in the cart
        cart = request.session.get('cart', {})
        for item in cart.values():
            item_qty = item['quantity']
            product = get_object_or_404(Product, pk=item['product_id'])
            total_price = product.price * item_qty

            cart_item, created = Cart.objects.get_or_create(
                user=request.user, product=product, defaults={'quantity': item['quantity']})

            order = Order.objects.create(customer=user_r, orderitem=cart_item, quantity=cart_item.quantity,
                                         shipping=shipping_Address, total_price=total_price, status="pending")

            order.save()
            product.quantity -= item_qty
            product.save()
            if not created:
                cart_item.quantity += item['quantity']
                cart_item.save()

        # Send email to the customer with order details
        order_details = f"Mr/Mrs: {user_r.username} \n\nYour Order details \nOrder ID: {order.id}\n\n"
        order_details += "Order Items:\n"
        for item in cart.values():
            product = Product.objects.get(pk=item['product_id'])
            order_details += f"\nProduct: {product.product_name},\nQuantity: {item['quantity']}, Price:{product.price}, Total:{ product.price * item['quantity']} \n"
        order_details += "\n\nThanks For Purchasing."
        send_mail(
            'Order Confirmation',
            order_details,
            'asgharabbasikalhoro@gmail.com',  # Replace with your email address
            [user_r.email],  # Send email to the customer's email address
            fail_silently=False,
        )

        # Clear the cart in the session
        request.session['cart'] = {}
        messages.success(request, 'Your order has been placed!')
        return redirect('product_list')

    # Display the items in the cart
    cart_items = []
    cart = request.session.get('cart', {})
    for item in cart.values():
        product = Product.objects.get(pk=item['product_id'])
        cart_items.append({'product': product, 'quantity': item['quantity']})

    context = {'cart_items': cart_items}
    return render(request, 'cart.html', context)


def remove_from_cart(request, product_id):
    print("rem :", product_id)

    product_id = str(product_id)
    # cart = request.session['cart'] # both works
    cart = request.session.get('cart', {})

    print(cart)
    if product_id in cart:
        print("  if product_id in cart: ", product_id in cart)
        del cart[product_id]
        request.session['cart'] = cart
    return redirect('cart')

# @login_required(login_url='login_user')
# def remove_from_cart(request, cart_id):
#     cart_item = get_object_or_404(Cart, pk=cart_id)
#     if cart_item.user == request.user:
#         cart_item.delete()
#     return redirect('cart')


@login_required(login_url='login_user')
def ShippingAddress(request):
    print("\n in shipping ad \n ")
    print("request.method :", request.method)
    if request.method == 'POST':
        contact = request.POST.get('contact')
        shipping_address = request.POST.get('shipping_address')
        shipping_city = request.POST.get('shipping_city')
        shipping_state = request.POST.get('shipping_state')
        shipping_country = request.POST.get('shipping_country')
        shipping_zip_code = request.POST.get('shipping_zip_code')
        print(shipping_address, shipping_city, shipping_state,
              shipping_country, shipping_zip_code)

        # Create a new ShippingAddress object with the submitted data
        new_shipping_address = Shipping_Address(
            customer=request.user,
            contact=contact,
            shipping_address=shipping_address,
            shipping_city=shipping_city,
            shipping_state=shipping_state,
            shipping_country=shipping_country,
            shipping_zip_code=shipping_zip_code
        )

        # Save the new ShippingAddress object to the database
        new_shipping_address.save()
        return
    else:
        # If the request method is not POST, render the shipping address form
        return render(request, 'shipping_address_form.html')


# @login_required(login_url='login_user')
# def cart(request):
#     user_r = request.user
#     cart_items = Cart.objects.filter(user=user_r)

#     # total_price = cart_tags.total_price_products(cart_items)
#     # shipping_address = Shipping_Address.objects.get(customer=user)

#     if request.method == "POST":
#         # if not request.user.is_authenticated:

#         # total_price = cart_tags.total_price_products(cart_items)
#         ShippingAddress(request)
#         print("user1 :", user_r)
#         print("cart_items1 :", cart_items)
#         shipping_Address = Shipping_Address.objects.filter(customer=user_r)[0]

#         print("shipping_Address1 :", shipping_Address)
#         for cart_item in cart_items:
#             total_price = cart_item.product.price * cart_item.quantity
#             order = Order.objects.create(customer=user_r, orderitem=cart_item, quantity=cart_item.quantity,
#                                          shipping=shipping_Address, total_price=total_price, status='Pending')

#             order.save()
#         # cart_item = get_object_or_404(Cart, pk=cart_item.id)
#         # cart_items.delete()
#         for cart_item in cart_items:
#             cart_it = get_object_or_404(Cart, pk=cart_item.id)
#             # if cart_it.user == request.user:
#             #     cart_it.delete()

#     return render(request, 'cart.html', {'cart_items': cart_items})
