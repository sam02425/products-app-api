"""
Views for the recipe APIs
"""
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import (
    viewsets,
    mixins,)

from core.models import (Product, Tag, Ingredient, Size, Category,)
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


class TagViewSet(mixins.DestroyModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    """ViewSet for the Tag class."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve the tags for the authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    # def get_Serializer_class(self):
    #     """Add the request user to the serializer context."""
    #     if self.action == 'list':
    #         return serializers.TagSerializer

    #     return self.serializer_class

    def perform_create(self, serializer):
        """Create a new tag for the authenticated user."""
        serializer.save(user=self.request.user)


class IngredientViewSet(mixins.ListModelMixin,
                        viewsets.GenericViewSet,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin):
    """Manage ingredients in the database."""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new ingredient for the authenticated user."""
        serializer.save(user=self.request.user)


class SizeViewSet(mixins.ListModelMixin,
                viewsets.GenericViewSet,
                mixins.CreateModelMixin,
                mixins.DestroyModelMixin,
                mixins.UpdateModelMixin):
    """Manage sizes in the database."""
    serializer_class = serializers.SizeSerializer
    queryset = Size.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new size for the authenticated user."""
        serializer.save(user=self.request.user)


class CategoryViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin):
    """Manage categories in the database."""
    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new category for the authenticated user."""
        serializer.save(user=self.request.user)

