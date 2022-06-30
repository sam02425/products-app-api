"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import (
    Product,
    Tag,
    Ingredient,
    Size,
    Category,
    Manufacturer,)


class ManufacturerSerializer(serializers.ModelSerializer):
    """Serializer for the Manufacturer class."""

    class Meta:
        model = Manufacturer
        fields = ('id', 'name', 'description')
        read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for ingredients."""

    class Meta:
        model = Category
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']


class SizeSerializer(serializers.ModelSerializer):
    """Serializer for ingredients."""

    class Meta:
        model = Size
        fields = ['id', 'name', 'description' , 'product_Type', 'amount', 'amount_Unit','created_At', 'updated_At']
        read_only_fields = ['id']


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredients."""

    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'description', 'ingredient_Amount','ingredient_Amount_Unit', 'created_At', 'updated_At']
        read_only_fields = ['id']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for creating tags."""

    class Meta:
        model = Tag
        fields = ['id','name', 'description','created_At', 'updated_At']
        read_only_fields = ['id']


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for product objects."""
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)
    sizes = SizeSerializer(many=True, required=False)
    category = CategorySerializer(required=False)
    manufacturer = ManufacturerSerializer(required=False)


    class Meta:
        model = Product
        fields = ['id', 'name','brand','description','price', 'weight' ,'stock', 'availability', 'link','sizes', 'tags','ingredients','category','manufacturer', 'created_At', 'created_By', 'updated_At', 'updated_By']
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

    def _get_or_create_ingredients(self, product, ingredients):
        """Create and add ingredients to a product."""
        auth_user = self.context['request'].user
        for ingredient in ingredients:
            ingredient_obj, created = Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient,
            )
            product.ingredients.add(ingredient_obj)

    def _get_or_create_sizes(self, product, sizes):
        """Create and add ingredients to a product."""
        auth_user = self.context['request'].user
        for sizes in sizes:
            size_obj, created = sizes.objects.get_or_create(
                user=auth_user,
                **sizes,
            )
            product.ingredients.add(size_obj)

    def _get_or_create_category(self, product, category):
        """Create and add ingredients to a product."""
        auth_user = self.context['request'].user
        for category in category:
            category_obj, created = category.objects.get_or_create(
                user=auth_user,
                **category,
            )
            product.ingredients.add(category_obj)

    def _get_or_create_manufacturer(self, product, manufacturer):
        """Create and add ingredients to a product."""
        auth_user = self.context['request'].user
        for manufacturer in manufacturer:
            manufacturer_obj, created = manufacturer.objects.get_or_create(
                user=auth_user,
                **manufacturer,
            )
            product.ingredients.add(manufacturer_obj)


    def create(self, validated_data):
        """Create a new product."""
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])
        sizes = validated_data.pop('sizes', [])
        category = validated_data.pop('category', None)
        manufacturer = validated_data.pop('manufacturer', None)
        product = Product.objects.create(**validated_data)
        self._get_or_create_tags(product, tags)
        self._get_or_create_ingredients(product, ingredients, sizes, category, manufacturer)

        return product

    def update(self, instance, validated_data):
        """Update a product."""

        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredients', None)
        sizes = validated_data.pop('sizes', None)
        category = validated_data.pop('category', None)
        manufacturer = validated_data.pop('manufacturer', None)

        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(instance, tags)

        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(instance, ingredients)

        if sizes is not None:
            instance.sizes.clear()
            self._get_or_create_sizes(instance, sizes)

        if category is not None:
            instance.category.clear()
            self._get_or_create_category(instance, category)

        if manufacturer is not None:
            instance.manufacturer.clear()
            self._get_or_create_manufacturer(instance, manufacturer)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

