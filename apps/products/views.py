from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer, ProductCreateSerializer, ProductListSerializer
from users.permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

class ProductCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
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
            if not request.user.is_admin:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("You do not have permission to access all data.")
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        return super().list(request, *args, **kwargs)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.filter(deleted_at__isnull=True).prefetch_related('skus__size', 'skus__color', 'images')
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            # Only admins can update or delete
            permission_classes = [IsAdmin]
        else:
            # Anyone can retrieve
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]


    def get_serializer_context(self):   
        return {'request': self.request}