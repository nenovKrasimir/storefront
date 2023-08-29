from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView

from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


class ProductList(ListCreateAPIView):
    
    '''We can use 'queryset =' and 'serliazer_class ='
       if we dont have any extra logic like if statements'''

    def get_queryset(self):
        return Product.objects.all().select_related('collection').all()
    
    def get_serializer_class(self):
        return ProductSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}


class ProductDetails(APIView):

    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitem_set.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CollectionList(ListCreateAPIView):

    def get_queryset(self):
        return Collection.objects.annotate(products_count=Count('product'))
    
    def get_serializer_class(self):
        return CollectionSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}


@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(
        Collection.objects.annotate(
        products_count=Count('product')), pk=pk)
        
    if request.method == 'GET':
        seriliazer = CollectionSerializer(collection)
        return Response(seriliazer.data)
    
    elif request.method == 'PUT':
        seriliazer = CollectionSerializer(collection, data=request)
        seriliazer.is_valid(raise_exception=True)
        seriliazer.save()
        return Response(seriliazer.data)
    
    elif request.method == 'DELETE':
        if collection.product.count() > 0:
            return Response({'error': 'Collection cannot be deleted because their is products related to the collection'})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)