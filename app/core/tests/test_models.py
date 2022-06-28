"""
Tests for models.
"""
from decimal import Decimal
from pydoc import describe

from unittest import expectedFailure
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def create_user(email="user@example.com", password="trial12345"):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is mormalized for new users"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','test123')

    def test_create_superuser(self):
        """Test creating a surper user"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_product(self):
        """Test creating a recipe"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'test123',
        )

        # size = models.Size.objects.create(
        #     name='Small',
        #     weight=Decimal('0.5'),
        # )

        # manufacturer= models.Manufacturer.objects.create(
        #     name='Test Manufacturer',
        # )

        # category = models.Category.objects.create(
        #     name='Test Catagory',
        # )

        product = models.Product.objects.create(
            user=user,
            name='Steak',
            brand='Test Brand',
            stock=10,
            availability=True,
            weight = Decimal('1.0'),
            price=Decimal('5.00'),
            description='Steak for dinner',
        )

        self.assertEqual(str(product), product.name)

    def test_create_tags(self):
        """Test creating a tag"""
        tag = models.Tag.objects.create(
            user=create_user(),
            name='Vegan',
        )

        self.assertEqual(str(tag), tag.name)

    def test_create_ingridients(self):
        """Test creating an ingridient"""
        ingredient = models.Ingredient.objects.create(
            user=create_user(),
            name='Salt',
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_create_size(self):
        """Test creating a size"""
        size = models.Size.objects.create(
            user=create_user(),
            name='Small',
            product_Type='powder',
            amount=Decimal('0.5'),
            amount_Unit='kg',
        )

        self.assertEqual(str(size), size.name)

    def test_category_str(self):
        """Test the category string representation"""
        category = models.Category.objects.create(
            user=create_user(),
            name='Test Category',
        )

        self.assertEqual(str(category), category.name)