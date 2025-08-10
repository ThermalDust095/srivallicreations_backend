from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    inStock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    youtubeUrl = models.URLField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __ster__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    is_primary = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)

class ProductAttribute(models.Model):
    ATTRIBUTE_TYPES = [
        ('size', 'Size'),
        ('color', 'Color'),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=ATTRIBUTE_TYPES)

    def __str__(self):
        return self.name

class ProductSKU(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, related_name='skus', on_delete=models.CASCADE)
    size = models.ForeignKey(ProductAttribute, on_delete=models.PROTECT, related_name= 'color', limit_choices_to={'type': 'size'})
    color = models.ForeignKey(ProductAttribute, on_delete=models.PROTECT,related_name= 'size',limit_choices_to={'type': 'color'})
    stock = models.PositiveIntegerField(default=0)