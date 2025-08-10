from django.urls import path
from .views import ProductListView, ProductDetailView, ProductCreateView

urlpatterns = [
    path('product/', ProductListView.as_view(), name='product-list'),
    path('product/<uuid:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('product-create/', ProductCreateView.as_view(), name='product-create'),
]
