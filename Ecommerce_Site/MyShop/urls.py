"""
URL configuration for Ecommerce_Site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static

# app_name = 'MyShop'


urlpatterns = [
    path('', views.product_list, name='product_list'),

    path('customers/<int:customer_id>', views.customer_detail, name='customer_detail'),
    path('products/<int:product_id>', views.product_detail, name='product_detail'),
    path('add-product', views.create_product, name='add-product'),

    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/create', views.create_order, name='create_order'),
    path('product/<int:product_id>/add_to_cart/',views.add_to_cart, name='add_to_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove_from_cart/<int:cart_id>/',views.remove_from_cart, name='remove_from_cart'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
