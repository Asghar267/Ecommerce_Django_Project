from django import template
register = template.Library()

# @register.filter(name='cart_total')
# def cart_total(cart):
#     total = sum(item.product.price * item.quantity for item in cart)
#     return total

 
@register.filter
def total_price(cart_items): # total of product item quantity
    sum = cart_items.product.price * cart_items.quantity
    print(cart_items.product.price * cart_items.quantity,"sum :",sum)
    return  sum

@register.filter
def total_price_products(cart_items): # total of all products
    return sum(item.product.price * item.quantity for item in cart_items)
    
