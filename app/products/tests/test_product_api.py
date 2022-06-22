"""
    Test Product API
"""

from decimal import Decimal
from os import link

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import status
from rest_framework.test import APIClient

from core.models import Product

from products.serializers import ProductSerializer

PRODUCT_URL = reverse('products:product-list')

def create_product(user, **params):
    """Create and return a new product."""
    defaults = {
        'name': 'Test Product',
        'description': 'Test description',
        'price': Decimal('10.00'),
        'weight': Decimal('1.00'),
        'stock': 10,
        'avalability': True,
        'category': 'Test Category',
        'manufacturer': 'Test Manufacturer',
        'size': 'Small',
        link: 'http://example.com',
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
            'testpass'
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
            'testpass2'
        )
        create_product(other_user)
        product = create_product(self.user)
