"""
Views for the recipe APIs
"""
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import (
    viewsets,
    mixins,)

from core.models import (Product, Tag, Ingredient, Size, Category, Manufacturer,)
from products import serializers


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for the Product class."""
    serializer_class = serializers.ProductDetailSerializer
    queryset = Product.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve the recipes for the authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_Serializer_class(self):
        """Add the request user to the serializer context."""
        if self.action == 'list':
            return serializers.ProductSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new product for the authenticated user."""
        serializer.save(user=self.request.user)


class BaseProductAtteributiveViewSet(mixins.DestroyModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.ListModelMixin,
                                    viewsets.GenericViewSet):
    """Base viewset for user owned recipe attributes."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
            """Filter queryset to authenticated user."""
            return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new product for the authenticated user."""
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """Create a new product for the authenticated user."""
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        """Delete a product for the authenticated user."""
        instance.delete()


class TagViewSet(BaseProductAtteributiveViewSet):
    """ViewSet for the Tag class."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseProductAtteributiveViewSet):
    """Manage ingredients in the database."""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()


class SizeViewSet(BaseProductAtteributiveViewSet):
    """Manage sizes in the database."""
    serializer_class = serializers.SizeSerializer
    queryset = Size.objects.all()


class CategoryViewSet(BaseProductAtteributiveViewSet):
    """Manage categories in the database."""
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()


class ManufacturerViewSet(BaseProductAtteributiveViewSet):
    """ViewSet for the ProductCategory class."""
    serializer_class = serializers.ManufacturerSerializer
    queryset = Manufacturer.objects.all()

