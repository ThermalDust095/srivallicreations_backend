from rest_framework import serializers
from .models import Product, ProductAttribute, ProductSKU, ProductImage
import json


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary']
    
    def get_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['id', 'name', 'type']

class ProductSKUSerializer(serializers.ModelSerializer):
    size = serializers.CharField()
    color = serializers.CharField()
    stock = serializers.IntegerField()
    class Meta:
        model = ProductSKU
        fields = ['size', 'color', 'stock']

class ProductListSerializer(serializers.ModelSerializer):
        primary_image = serializers.SerializerMethodField(read_only=True)
        sizes = serializers.SerializerMethodField(read_only=True)
        colors = serializers.SerializerMethodField(read_only=True)
        class Meta:
            model = Product
            fields = ['id', 'name', 'price', 'category', 'inStock', 'featured', 'sizes', 'colors', 'primary_image' ,'createdAt']

        def get_primary_image(self, obj):
            request = self.context.get('request')
            primary_image = obj.images.filter(is_primary=True).first()
            if primary_image and request:
                return request.build_absolute_uri(primary_image.image.url)
            return None
        
        def get_sizes(self, obj):
            sizes = obj.skus.values_list('size__name', flat=True).distinct()
            return list(sizes)
        
        def get_colors(self, obj):
            colors = obj.skus.values_list('color__name', flat=True).distinct()
            return list(colors)

class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)
    primary_image = serializers.SerializerMethodField()
    skus = ProductSKUSerializer(many=True, required=False)

    image_files = serializers.ListField(
        child=serializers.ImageField(max_length=None, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 
            'inStock', 'featured', 'youtubeUrl', 'createdAt', 'deleted_at', 'images', 'primary_image', 'skus','image_files']

    def get_primary_image(self, obj):
        request = self.context.get('request')
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image and request:
            return request.build_absolute_uri(primary_image.image.url)
        return None
    
    def get_images(self, obj):
        request = self.context.get('request')
        images = []
        for image in obj.images.all():
            if image.image and request:
                images.append(request.build_absolute_uri(image.image.url))
        return images
    
    def update(self, instance, validated_data):
        images_data = validated_data.pop('image_files', [])
        skus_raw = self.initial_data.get('skus')
        if isinstance(skus_raw, str):
            try:
                skus_data = json.loads(skus_raw)
            except Exception:
                skus_data = []
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        
        if skus_data != []: # Clear existing SKUs
            instance.skus.all().delete() 
            for sku in skus_data:
                size_name = sku['size']
                color_name = sku['color'].upper()
                stock = sku['stock']

                try:
                    size = ProductAttribute.objects.get(name=size_name, type='size')
                    color = ProductAttribute.objects.get(name=color_name, type='color')
                except ProductAttribute.DoesNotExist:
                    continue  # skip invalid size/color

                ProductSKU.objects.update_or_create(
                    product=instance,
                    size=size,
                    color=color,
                    defaults={'stock': stock}
                )

        if images_data != []:
            instance.images.all().delete()  # Clear existing images
            for i, image_file in enumerate(images_data):
                ProductImage.objects.update_or_create(
                        product=instance,
                        image=image_file,
                        is_primary=(i == 0)  # First image is primary
                )
        
        return instance

class ProductCreateSerializer(serializers.ModelSerializer):
    skus = serializers.JSONField(write_only=True, required=False)
    image_files = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'inStock', 'featured',
                  'youtubeUrl', 'skus', 'image_files']

    def create(self, validated_data):
        skus_data = validated_data.pop('skus', [])
        images_data = validated_data.pop('image_files', [])

        product = Product.objects.create(**validated_data)

        # Handle SKUs
        for sku in skus_data:
            size_name = sku['size']
            color_name = sku['color'].upper()
            stock = sku['stock']

            try:
                size = ProductAttribute.objects.get(name=size_name, type='size')
                color = ProductAttribute.objects.get(name=color_name, type='color')
            except ProductAttribute.DoesNotExist:
                continue  # skip invalid size/color

            ProductSKU.objects.create(
                product=product,
                size=size,
                color=color,
                stock=stock
            )

        # Handle images
        for i, image_file in enumerate(images_data):
            ProductImage.objects.create(
                product=product,
                image=image_file,
                is_primary=(i == 0)  # First image is primary
            )

        return product
