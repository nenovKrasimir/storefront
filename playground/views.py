from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product, Customer, Collection
# Create your views here.

def say_hello(request):
    exists = Customer.objects.filter(email__icontains='com')
    collections_contains = Collection.objects.filter(featured_product__isnull=True)
    products_low_inventory = Product.objects.filter(inventory__lt=10)


    return render(request, 'hello.html', {
        'customers': exists,
        'collections': collections_contains,
        'low_inventory_products': products_low_inventory
            }
            )
