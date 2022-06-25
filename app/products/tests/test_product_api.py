"""
    Test Product API
"""

from decimal import Decimal
from genericpath import exists
from os import link

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (Product, Tag)
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
        'category': 'food',
        'manufacturer': 'xyz',
        'size': 'small',
        'link': 'http://example.com',
    }
    defaults.update(params)

    product = Product.objects.create(user=user, **defaults)
    return product

def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


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
        self.user = create_user(email='user@example.com', password='password123')
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
        other_user = create_user(email='other@example.com',
            password='password123',
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

    def test_create_basic_product(self):
        """Test creating a product."""
        payload = {
            'name': 'Test Product',
            'description': 'Test description',
            'price': Decimal('10.00'),
            'weight': Decimal('1.00'),
            'stock': 10,
            'availability': True,
            'category': 'food',
            'manufacturer': 'xyz',
            'size': 'small',
            'link': 'http://example.com',
        }
        res = self.client.post(PRODUCT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(product, k), v)
        self.assertEqual(product.user, self.user)

    def test_partial_update(self):
        """Test updating a product with patch."""
        original_link = 'http://example.com/product.pdf'
        product = create_product(
            user = self.user,
            name = 'Test Product',
            link = original_link,
            )

        payload = {'name': 'New name'}
        url = product_detail_url(product.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        product.refresh_from_db()
        self.assertEqual(product.name, payload['name'])
        self.assertEqual(product.link, original_link)
        self.assertEqual(product.user, self.user)

    # def test_full_update(self):
    #     """Test updating a product with put."""
    #     original_link = 'http://example.com/product.pdf'
    #     product = create_product(
    #         user = self.user,
    #         name = 'Test Product',
    #         link = original_link,
    #     )

    #     payload = {
    #         'name': 'New name 2',
    #         'link': 'http://example.com/new.pdf',
    #         'description': 'New description',
    #     }
    #     url = product_detail_url(product.id)
    #     res = self.client.put(url, payload)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     product.refresh_from_db()
    #     for k, v in payload.items():
    #         self.assertEqual(getattr(product, k), v)
    #     self.assertEqual(product.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the product user results in an error."""
        new_user = create_user(email='user2@example.com', password='password123')
        product = create_product(user = self.user)
        payload = {'user': new_user.id}
        url = product_detail_url(product.id)
        self.client.patch(url, payload)

        product.refresh_from_db()
        self.assertEqual(product.user, self.user)

    def test_delete_product(self):
        """Test deleting a product."""
        product = create_product(user = self.user)
        url = product_detail_url(product.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.filter(id=product.id).exists(), False)

    def test_product_other_users_recipe_error(self):
        """Test trying to delete another users recipe gives error."""
        new_user = create_user(email='user2@example.com', password='test123')
        product = create_product(user = new_user)

        url = product_detail_url(product.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Product.objects.filter(id=product.id).exists(), True)

    def test_create_product_with_tags(self):
        """Test creating a product with tags."""
        payload = {
            'name': 'Test Product',
            'description': 'Test description',
            'price': Decimal('10.00'),
            'weight': Decimal('1.00'),
            'stock': 10,
            'availability': True,
            'category': 'food',
            'manufacturer': 'xyz',
            'size': 'small',
            'link': 'http://example.com',
            'tags': [{"name": 'healthy'}, {"name": 'fastfood'}]
        }
        res = self.client.post(PRODUCT_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        product = Product.objects.filter(user=self.user)
        self.assertEqual(product.count(), 1)
        product = product[0]
        self.assertEqual(product.tags.count(), 2)
        for tag in payload['tags']:
            exists = Tag.objects.filter(
                user=self.user,
                name=tag['name']
            ).exists()
            self.assertTrue(exists)

    def test_create_product_with_existing_tags(self):
        """Test creating a product with existing tags."""
        tag_meat_conitained = Tag.object.create_tag(user=self.user, name='meat')
        payload = {
            'name': 'Test Product',
            'description': 'Test description',
            'price': Decimal('10.00'),
            'weight': Decimal('1.00'),
            'stock': 10,
            'availability': True,
            'category': 'food',
            'manufacturer': 'xyz',
            'size': 'small',
            'link': 'http://example.com',
            'tags': [{"name": 'meat'}, {"name": 'fastfood'}]
        }
        res = self.client.post(PRODUCT_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        product = Product.objects.filter(user=self.user)
        self.assertEqual(product.count(), 1)
        product = product[0]
        self.assertEqual(product.tags.count(), 2)
        self.assertEqual(product.tags.all(), tag_meat_conitained.name)
        for tag in payload['tags']:
            exists = Tag.objects.filter(
                user=self.user,
                name=tag['name']
            ).exists()
            self.assertTrue(exists)