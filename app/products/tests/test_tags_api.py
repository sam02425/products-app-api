"""
Tests for Tag api
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Tag

from products.serializers import TagSerializer

TAGS_URL = reverse('products:tag-list')


def detail_url(tag_id):
    """Return tag detail URL"""
    return reverse('products:tag-detail', args=[tag_id])


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email=email, password=password)

def PublicTagsApiTests(TestCase):
    """Test the public tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

def PrivateTagsApiTests(TestCase):
    """Test the authorized user tags API"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Tag.objects.create(user=self.user, name='Vegan', description='Vegan food', created_At= '4/5/2019', updated_At='4/5/2020')
        Tag.objects.create(user=self.user, name='Dessert', description='Desserts', created_At= '4/5/2019', updated_At='4/5/2020')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for the authenticated user"""
        user2 = create_user(
            email='user2@example.com', password='testpass123'
        )
        Tag.objects.create(user=user2, name='Fruity', description='Fruity food',created_At= '4/5/2019', updated_At='4/5/2020')
        tag = Tag.objects.create(user=self.user, name='Comfort Food', description='Good for you', created_At= '4/5/2019', updated_At='4/5/2020')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)

    def test_update_tag(self):
        """Test updating a tag with a patch request"""
        tag = Tag.objects.create(user=self.user, name='Vegitarian', description='Vegan food', created_At= '4/5/2019', updated_At='4/5/2020')

        payload = {'name': 'Vegan', 'description': 'Vegan food', 'created_At': '4/5/2019', 'updated_At': '4/5/2020'}
        url = detail_url(tag.id)
        res = self.client.patch(url, payload)

        tag.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(tag.name, payload['name'])


    def test_delete_tag(self):
        """Test deleting a tag"""
        tag = Tag.objects.create(user=self.user, name='Vegan', description='Vegan food',created_At= '4/5/2019', updated_At='4/5/2020')

        url = detail_url(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tags = Tag.objects.filter(user=tag.user)
        self.assertFalse(tags.exists())
