"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import (
    Product,
    Tag)


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for product objects."""

    class Meta:
        model = Product
        fields = ['id', 'name', 'description','price', 'weight', 'stock', 'availability', 'category', 'manufacturer', 'size', 'link']
        read_only_fields = ['id']


class ProductDetailSerializer(ProductSerializer):
    """Serializer for product detail objects."""

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['description']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for creating tags."""

    class Meta:
        model = Tag
        fields = ['name'],
        read_only_fields = ['id']
