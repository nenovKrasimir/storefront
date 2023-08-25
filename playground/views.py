from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product, Customer, Collection, OrderItem

# Create your views here.

def say_hello(request):
    exists = Customer.objects.filter(email__icontains='com')
    collections_contains = Collection.objects.filter(featured_product__isnull=True)
    products_low_inventory = Product.objects.filter(inventory__lt=10)
    ordered_and_sorted = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')

    context =  {
        'customers': exists,
        'collections': collections_contains,
        'low_inventory_products': products_low_inventory,
        'ordered_and_sorted': ordered_and_sorted,
        'query_set': ordered_and_sorted
        }


    return render(request, 'hello.html', context=context)
