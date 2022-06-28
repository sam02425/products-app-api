"""
Tests for the sizes API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Size

from products.serializers import SizeSerializer


SIZE_URL = reverse('products:size-list')


def create_user(email='user@example.com', password='testpass123'):
    """Create and return user."""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicsizesApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving sizes."""
        res = self.client.get(SIZE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatesizesApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_sizes(self):
        """Test retrieving a list of sizes."""
        Size.objects.create(user=self.user, name='small', description='small size', product_Type='liquid', amount=1, amount_Unit='ml')
        Size.objects.create(user=self.user, name='large', description='large size', product_Type='liquid', amount=1, amount_Unit='ml')

        res = self.client.get(SIZE_URL)

        sizes = Size.objects.all().order_by('-name')
        serializer = SizeSerializer(sizes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_sizes_limited_to_user(self):
        """Test list of sizes is limited to authenticated user."""
        user2 = create_user(email='user2@example.com')
        Size.objects.create(user=user2, name='small', description='small size', product_Type='liquid', amount=1, amount_Unit='ml')
        size = Size.objects.create(user=self.user, name='xlarge', description='large size', product_Type='powder', amount=1, amount_Unit='ml')

        res = self.client.get(SIZE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], size.name)
        self.assertEqual(res.data[0]['id'], size.id)
