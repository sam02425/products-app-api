"""
    Test Product API
"""

from decimal import Decimal
from os import link

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Product
from core import models

from products.serializers import (
    ProductSerializer,
    ProductDetailSerializer)

PRODUCT_URL = reverse('products:product-list')


def product_detail_url(product_id):
    """Return product detail URL"""
    return reverse('products:product-detail', args=[product_id])

def create_product(user, **params):
    """Create and return a new product."""
    defaults = {
        'name': 'Test Product',
        'description': 'Test description',
        'price': Decimal('10.00'),
        'weight': Decimal('1.00'),
        'stock': 10,
        'availability': True,
        'category': models.Category.objects.create(name='Test Category'),
        'manufacturer': models.Manufacturer.objects.create(name='Test Manufacturer'),
        'size': models.Size.objects.create(size='Small', weight=Decimal('0.5')),
        'link': 'http://example.com',
    }
    defaults.update(params)

    product = Product.objects.create(user=user, **defaults)
    return product


class PublicProductApiTests(TestCase):
    """Test unauthenticated product API access."""

    def setUp(self):
            self.client = APIClient()

    def test_required_auth(self):
            """Test the authentication is required."""
            res = self.client.get(PRODUCT_URL)

            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateProductApiTests(TestCase):
    """Test authenticated product API access."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_product(self):
        """Test retrieving a list of products."""
        create_product(self.user)
        create_product(self.user)

        res = self.client.get(PRODUCT_URL)

        products = Product.objects.all().order_by('-id')
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_products_list_limited_to_user(self):
        """Test retrieving products for user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        create_product(user = other_user)
        create_product(user = self.user)

        res = self.client.get(PRODUCT_URL)

        products = Product.objects.filter(user=self.user)
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_product_detail(self):
        """Test retrieving a product detail."""
        product = create_product(user = self.user)

        url = product_detail_url(product.id)
        res = self.client.get(url)

        serializer = ProductDetailSerializer(product)
        self.assertEqual(res.data, serializer.data)
