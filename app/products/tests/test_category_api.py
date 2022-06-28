"""
Tests for the categorys API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Category

from products.serializers import CategorySerializer


CATEGORY_URL = reverse('products:category-list')


def create_user(email='user@example.com', password='testpass123'):
    """Create and return user."""
    return get_user_model().objects.create_user(email=email, password=password)


class PubliccategorysApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving categorys."""
        res = self.client.get(CATEGORY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatecategorysApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_categorys(self):
        """Test retrieving a list of categorys."""
        Category.objects.create(user=self.user, name='DRINKS')
        Category.objects.create(user=self.user, name='MILK')

        res = self.client.get(CATEGORY_URL)

        categorys = Category.objects.all().order_by('-name')
        serializer = CategorySerializer(categorys, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_categorys_limited_to_user(self):
        """Test list of categorys is limited to authenticated user."""
        user2 = create_user(email='user2@example.com')
        Category.objects.create(user=user2, name='FOOD')
        category = Category.objects.create(user=self.user, name='VEGIETABLES')

        res = self.client.get(CATEGORY_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], category.name)
        self.assertEqual(res.data[0]['id'], category.id)
