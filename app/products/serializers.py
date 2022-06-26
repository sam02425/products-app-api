"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import (
    Product,
    Tag)


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
        fields = ['id', 'name', 'description','price', 'weight', 'stock', 'availability', 'category', 'manufacturer', 'size', 'link', 'tags']
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

    def create(self, validated_data):
        """Create a new product."""
        tags = validated_data.pop('tags', [])
        product = Product.objects.create(**validated_data)
        self._get_or_create_tags(product, tags)

        return product

    def update(self, instance, validated_data):
        """Update a product."""

        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(instance, tags)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

