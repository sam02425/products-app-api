"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import (
    Product,
    Tag,
    Manufacturer,)


class ManufacturerSerializer(serializers.ModelSerializer):
    """Serializer for Manufacturer objects"""

    class Meta:
        model = Manufacturer
        fields = ('id', 'name',)
        read_only_fields = ['id']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for creating tags."""

    class Meta:
        model = Tag
        fields = ['id','name']
        read_only_fields = ['id']


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for product objects."""
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ['id', 'name', 'brand', 'description', 'aisle', 'rack_number', 'size', 'stock', 'weight', 'unit', 'availability', 'price', 'category', 'sub_category', 'manufacturer', 'tags']
        read_only_fields = ['id']


class ProductDetailSerializer(ProductSerializer):
    """Serializer for product detail objects."""

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['description']


    def _get_or_create_tags(self, product, tags):
        """Create and add tags to a product."""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            product.tags.add(tag_obj)


    def _get_or_create_manufacturer(self, product, manufacturer):
        """Create and add manufacturer to a product."""
        auth_user = self.context['request'].user
        for manufacturer in manufacturer:
            manufacturer_obj, created = Manufacturer.objects.get_or_create(
                user=auth_user,
                **manufacturer,
            )
            product.manufacturer.add(manufacturer_obj)

    def create(self, validated_data):
        """Create a new product."""
        tags = validated_data.pop('tags', [])
        manufacturer = validated_data.pop('manufacturer', [])
        product = Product.objects.create(**validated_data)
        self._get_or_create_tags(product, tags, manufacturer)

        return product

    def update(self, instance, validated_data):
        """Update a product."""

        tags = validated_data.pop('tags', None)
        manufacturer = validated_data.pop('manufacturer', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(instance, tags)
        if manufacturer is not None:
            instance.manufacturer.clear()
            self._get_or_create_manufacturer(instance, manufacturer)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to recipes."""

    class Meta:
        model = Product
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}