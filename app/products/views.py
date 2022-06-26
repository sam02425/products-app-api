"""
Views for the recipe APIs
"""
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import (
    viewsets,
    mixins,)

from core.models import (Product, Tag)
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

    # def perform_create(self, serializer):
    #     """Create a new tag for the authenticated user."""
    #     serializer.save(user=self.request.user)