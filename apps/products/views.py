from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer, ProductCreateSerializer, ProductListSerializer

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    def get_serializer_context(self):
        return {'request': self.request}

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(deleted_at__isnull=True)
    serializer_class = ProductListSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.filter(deleted_at__isnull=True).prefetch_related('skus__size', 'skus__color', 'images')
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def get_serializer_context(self):   
        return {'request': self.request}