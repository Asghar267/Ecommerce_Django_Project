from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Customer, Product, Order, OrderItem, Payment
from .forms import ProductForm
# Create your views here.

 
def customer_detail(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    return render(request, 'customer_detail.html', {'customer': customer})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})

def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'order_detail.html', {'order': order, 'order_items': order_items})

def create_order(request):
    if request.method == 'POST':
        customer_id = request.POST['customer_id']
        customer = get_object_or_404(Customer, pk=customer_id)
        order = Order.objects.create(customer=customer, status='pending')
        for product_id in request.POST.getlist('product_id'):
            product = get_object_or_404(Product, pk=product_id)
            quantity = int(request.POST[f'product_{product_id}_quantity'])
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)
        payment_amount = order.total_price
        Payment.objects.create(order=order, amount=payment_amount)
        return HttpResponseRedirect(reverse('order_detail', args=(order.id,)))
    else:
        customers = Customer.objects.all()
        products = Product.objects.all()
        return render(request, 'create_order.html', {'customers': customers, 'products': products})


def create_product(request):
    if request.method == 'POST':
        print("Rquest: ",request)
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            # return redirect('product_list')
            print("product.pk :", product.pk)
            return redirect('product_detail', product)
        else:
            print("else create_product")
            return render(request, 'create_product.html', {'form': form})
    else:
        form = ProductForm()
    return render(request, 'create_product.html', {'form': form})

# class CreateProductView(View):
#     def get(self, request):
#         form = ProductForm()
#         return render(request, 'create_product.html', {'form': form})

#     def post(self, request):
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             product = form.save()
#             return redirect('product_detail', pk=product.pk)
#         else:
#             return render(request, 'create_product.html', {'form': form})

def add_to_cart(request, product_id):
    # Get the product object from the database
    product = get_object_or_404(Product, id=product_id)
    
    # Get the user's shopping cart from the session
    cart = request.session.get('cart', {})
    
    # Add the product to the cart or increment its quantity if it's already there
    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {'quantity': 1, 'price': str(product.price)}
    
    # Save the updated cart in the session
    request.session['cart'] = cart
    
    # Redirect the user back to the product page or wherever you want
    return redirect('product_detail', product_id=product_id)