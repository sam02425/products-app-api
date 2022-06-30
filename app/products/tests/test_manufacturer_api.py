"""
Tests for the manufacturer API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Manufacturer

from products.serializers import ManufacturerSerializer


MANUFACTURER_URL = reverse('products: manufacturer-list')


def create_user(email='user@example.com', password='testpass123'):
    """Create and return user."""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicmanufacturerApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving manufacturer."""
        res = self.client.get(MANUFACTURER_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatemanufacturerApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_manufacturer(self):
        """Test retrieving a list of manufacturer."""
        Manufacturer.objects.create(user=self.user, name='manufacturer', description='manufacturer description')
        Manufacturer.objects.create(user=self.user,  name='manufacturer2', description='manufacturer description')

        res = self.client.get(MANUFACTURER_URL)

        manufacturer = Manufacturer.objects.all().order_by('-name')
        serializer = ManufacturerSerializer(manufacturer, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_manufacturer_limited_to_user(self):
        """Test list of manufacturer is limited to authenticated user."""
        user2 = create_user(email='user2@example.com')
        Manufacturer.objects.create(user=user2,  name='manufacturer', description='manufacturer description')
        manufacturer = Manufacturer.objects.create(user=self.user,  name='manufacturer', description='manufacturer description')

        res = self.client.get(MANUFACTURER_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], manufacturer.name)
        self.assertEqual(res.data[0]['id'], manufacturer.id)
