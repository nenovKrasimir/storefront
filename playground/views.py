from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail, mail_admins, BadHeaderError
from django.db.models.aggregates import Count, Min, Sum
from store.models import Product, Customer, Collection, OrderItem, Order
from .tasks import notify_customers

# Create your views here.

def say_hello(request):
    notify_customers.delay('Hello')
    return render(request, 'hello.html', {'name': 'Mosh'})


    ### Exercies ### 

#     exists = Customer.objects.filter(email__icontains='com')
   
#     collections_contains = Collection.objects.filter(featured_product__isnull=True)
   
#     products_low_inventory = Product.objects.filter(inventory__lt=10)
   
#     ordered_and_sorted = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
   
#     order_count = Order.objects.aggregate(Orders_count=Count('id'))
   
#     sold_products = OrderItem.objects.filter(product_id=1).count()
   
#     orders_made_by_customer = Order.objects.filter(customer_id=1).count()

#     min_max_average_price = Product.objects.filter(collection_id=3)

#     order_item_mosh = OrderItem.objects.filter(product_id=1).aggregate(units_sold=Sum('quantity'))


#     context =  {
#         'customers': exists,
#         'collections': collections_contains,
#         'low_inventory_products': products_low_inventory,
#         'ordered_and_sorted': ordered_and_sorted,
#         'query_set': ordered_and_sorted,
#         'order_count': order_count,
#         'sold_products': sold_products,
#         'orders_made_by_customer': orders_made_by_customer,
#         'order_item_mosh' : order_item_mosh
#         }


#     return render(request, 'hello.html', context=context)
