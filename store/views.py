from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin

from .models import Product, Collection, OrderItem, Review, Cart, CartItem
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, AddCartItemSeriallzer, UpdateCartItemSerializer
from .filters import ProductFilter
from .pagination import DefaultPagination


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'last_update']

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because their is active order'})
    
        return super().destroy(request, *args, **kwargs)
    

class ColletionViewSet(ModelViewSet):
    
    queryset = Collection.objects.annotate(
        products_count=Count('product')
    ).all()
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.product.count() > 0:
            return Response({'error': 'Collection cannot be deleted because their is products related to the collection'})
        
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ReviewViewSet(ModelViewSet):
        serializer_class = ReviewSerializer

        def get_queryset(self):
            return Review.objects.filter(product_id=self.kwargs['product_pk'])
        def get_serializer_context(self):
            return {'product_id': self.kwargs['product_pk']}


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer
    lookup_field = 'id'  # Specify the field to use for lookup in the URL

    def retrieve(self, request, *args, **kwargs):
        cart = self.get_object()
        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSeriallzer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_id']}

    def get_queryset(self):
        return CartItem.objects\
            .filter(cart_id=self.kwargs['cart_id'])\
            .select_related('product')    

