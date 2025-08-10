from django.contrib import admin
from .models import Product, ProductImage, ProductAttribute, ProductSKU

# Register your models here.
admin.site.site_header = "SriValliCreations Admin"
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductAttribute)
admin.site.register(ProductSKU)
