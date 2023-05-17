from django import template
register = template.Library()
 
@register.filter
def total_price(cart_items): # total of product item quantity
    sum =  cart_items['quantity'] *cart_items['product'].price
    return sum


@register.filter
def price_total_profile(cart_items): # total of product item quantity
    sum =  cart_items.quantity *cart_items.total_price
    return sum

@register.filter
def total_price_products(cart_items): # total of all products
    sum =0
    for i in cart_items:
        sum += i['quantity']* i['product'].price
    return sum
    
