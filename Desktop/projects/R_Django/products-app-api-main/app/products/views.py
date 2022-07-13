"""
Views for the recipe APIs
"""
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import (
    viewsets,
    mixins,status,)

from rest_framework.decorators import action
from rest_framework.response import Response
from core.models import (Product, Tag, Manufacturer,)
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


    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to recipe."""
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseProductAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for recipe attributes."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')


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


class ManufacturerViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """ViewSet for the Manufacturer class."""
    serializer_class = serializers.ManufacturerSerializer
    queryset = Manufacturer.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
            """Retrieve the manufacturers for the authenticated user."""
            return self.queryset.filter(user=self.request.user).order_by('-name')

class TagViewSet(BaseProductAttrViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class ManufacturerViewSet(BaseProductAttrViewSet):
    """Manage manufacturers in the database."""
    serializer_class = serializers.ManufacturerSerializer
    queryset = Manufacturer.objects.all()




    # def get_Serializer_class(self):
    #     """Add the request user to the serializer context."""
    #     if self.action == 'list':
    #         return serializers.TagSerializer

    #     return self.serializer_class

    # def perform_create(self, serializer):
    #     """Create a new tag for the authenticated user."""
    #     serializer.save(user=self.request.user)