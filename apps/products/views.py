from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer, ProductCreateSerializer, ProductListSerializer
from rest_framework.response import Response

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
    
    def list(self, request, *args, **kwargs):
        if request.query_params.get('all-data') == 'true':
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        return super().list(request, *args, **kwargs)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.filter(deleted_at__isnull=True).prefetch_related('skus__size', 'skus__color', 'images')
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def get_serializer_context(self):   
        return {'request': self.request}