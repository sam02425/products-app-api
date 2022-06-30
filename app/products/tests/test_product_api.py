"""
    Test Product API
"""

from decimal import Decimal
from genericpath import exists
from os import link
import datetime


from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (Product, Tag, Manufacturer, Category, Ingredient,Size)
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
        'brand': 'Test Brand',
        'description': 'Test description',
        'price': Decimal('10.00'),
        'weight': Decimal('1.00'),
        'stock': 10,
        'availability': True,
        'link': 'http://example.com',
        'created_At': '4/5/2019',
        'created_By': user,
        'updated_At':'4/5/2020',
        'updated_By': user,
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
            'brand': 'Test Brand',
            'description': 'Test description',
            'price': Decimal('10.00'),
            'weight': Decimal('1.00'),
            'stock': 10,
            'availability': True,
            'link': 'http://example34.com',
            'created_At': '4/5/2019',
            'created_By': self.user,
            'updated_At':'4/5/2020',
            'updated_By': self.user
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

    # def test_create_product_with_tags(self):
    #     """Test creating a product with tags."""
    #     payload = {
    #         'name': 'Test Product',
            # 'brand': 'Test Brand',
            # 'description': 'Test description',
            # 'price': Decimal('10.00'),
            # 'weight': Decimal('1.00'),
            # 'stock': 10,
            # 'availability': True,
            # 'link': 'http://example.com',
    #         'tags': [{"name": 'healthy'}, {"name": 'fastfood'}]
    #     }
    #     res = self.client.post(PRODUCT_URL, payload)

    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     products = Product.objects.filter(user=self.user)
    #     self.assertEqual(products.count(), 1)
    #     product = products[0]
    #     self.assertEqual(product.tags.count(), 2)
    #     for tag in payload['tags']:
    #         exists = product.tags.filter(
    #             name=tag['name'],
    #             user=self.user,
    #         ).exists()
    #         self.assertTrue(exists)

    # def test_create_product_with_existing_tags(self):
    #     """Test creating a product with existing tags."""
    #     tag_meat_conitained = Tag.objects.create(user=self.user, name='meat')
    #     payload = {
    #         'name': 'Test Product',
    #         'description': 'Test description',
    #         'price': Decimal('10.00'),
    #         'weight': Decimal('1.00'),
    #         'stock': 10,
    #         'availability': True,
    #         'category': 'food',
    #         'manufacturer': 'xyz',
    #         'size': 'small',
    #         'link': 'http://example.com',
    #         'tags': [{"name": 'meat'}, {"name": 'fastfood'}],
    #     }
    #     res = self.client.post(PRODUCT_URL, payload)

    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     products = Product.objects.filter(user=self.user)
    #     self.assertEqual(products.count(), 1)
    #     product = products[0]
    #     self.assertEqual(product.tags.count(), 2)
    #     self.assertEqual(product.tags.all(), tag_meat_conitained.name)
    #     for tag in payload['tags']:
    #         exists = product.tags.filter(
    #             name=tag['name'],
    #             user=self.user,
    #         ).exists()
    #         self.assertTrue(exists)

    def test_create_tag_on_update(self):
        """Test creating a tag on update."""
        product = create_product(user = self.user)
        payload = {
            'tags': [{"name": 'Lunch'}]
        }
        url = product_detail_url(product.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_tag = Tag.objects.get(user=self.user, name='Lunch')
        self.assertIn(new_tag, product.tags.all())

    def test_update_product_assign_tag(self):
        """Test updating a product to assign a tag."""
        tag_meat_conitained = Tag.objects.create(user=self.user, name='meat')
        product = create_product(user = self.user)
        product.tags.add(tag_meat_conitained)

        tag_lunch = Tag.objects.create(user=self.user, name='Lunch')
        payload = {
            'tags': [{"name": 'Lunch'}]
            }
        url = product_detail_url(product.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(tag_lunch, product.tags.all())
        self.assertNotIn(tag_meat_conitained, product.tags.all())

    def test_clear_product_tags(self):
        """Test clearing a product tags."""
        tag = Tag.objects.create(user=self.user, name='Dessert')
        recipe = create_product(user=self.user)
        recipe.tags.add(tag)

        payload = {'tags': []}
        url = product_detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.tags.count(), 0)

    def test_create_recipe_with_new_ingredients(self):
        """Test creating a recipe with new ingredients."""
        payload = {
            'name': 'Test Product',
            'brand': 'Test Brand',
            'description': 'Test description',
            'price': Decimal('10.00'),
            'weight': Decimal('1.00'),
            'stock': 10,
            'availability': True,
            'ingredients': [{"name": 'Lemon'}, {"name": 'Sugar'}],
            'link': 'http://example.com',
            'created_At': '4/5/2019',
            'created_By': self.user,
            'updated_At':'4/5/2020',
            'updated_By': self.user,
        }
        res = self.client.post(PRODUCT_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        product = Product.objects.filter(user=self.user)
        self.assertEqual(product.count(), 1)
        recipe = product[0]
        self.assertEqual(recipe.ingredients.count(), 2)
        for ingredient in payload['ingredients']:
            exists = recipe.ingredients.filter(
                name=ingredient['name'],
                user=self.user,
            ).exists()
            self.assertTrue(exists)

    def test_create_recipe_with_existing_ingredient(self):
        """Test creating a new recipe with existing ingredient."""
        ingredient = Ingredient.objects.create(user=self.user, name='Lemon')
        payload = {
            'name': 'Test Product2',
            'brand': 'Test Brand2',
            'description': 'Test description',
            'price': Decimal('14.00'),
            'weight': Decimal('12.00'),
            'stock': 20,
            'availability': True,
            'link': 'http://example.com',
            'ingredients': [{"name": 'Lemon', 'ingredient_Amount': 1.0, 'ingredient_Amount_Unit': 'kg', 'description': 'Coriander is a good vegetable'}, {"name": 'Sugar','ingredient_Amount': 1.0, 'ingredient_Amount_Unit': 'kg', 'description': 'Coriander is a good vegetable'}],
            'created_At': '4/5/2019',
            'created_By': self.user,
            'updated_At':'4/5/2020',
            'updated_By': self.user,
        }
        res = self.client.post(PRODUCT_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Product.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        recipe = recipes[0]
        self.assertEqual(recipe.ingredients.count(), 2)
        self.assertIn(ingredient, recipe.ingredients.all())
        for ingredient in payload['ingredients']:
            exists = recipe.ingredients.filter(
                name=ingredient['name'],
                user=self.user,
            ).exists()
            self.assertTrue(exists)

    def test_create_ingredient_on_update(self):
        """Test creating an ingredient when updating a product."""
        recipe = create_product(user=self.user)

        payload = {'ingredients': [{'name': 'Limes'}]}
        url = product_detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_ingredient = Ingredient.objects.get(user=self.user, name='Limes')
        self.assertIn(new_ingredient, recipe.ingredients.all())

    def test_update_product_assign_ingredient(self):
        """Test assigning an existing ingredient when updating a product."""
        ingredient1 = Ingredient.objects.create(user=self.user, name='Pepper')
        product = create_product(user=self.user)
        product.ingredients.add(ingredient1)

        ingredient2 = Ingredient.objects.create(user=self.user, name='Chili')
        payload = {'ingredients': [{'name': 'Chili'}]}
        url = product_detail_url(product.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(ingredient2, product.ingredients.all())
        self.assertNotIn(ingredient1, product.ingredients.all())

    def test_clear_product_ingredients(self):
        """Test clearing a product ingredients."""
        ingredient = Ingredient.objects.create(user=self.user, name='Lemon')
        product = create_product(user=self.user)
        product.ingredients.add(ingredient)

        payload = {'ingredients': []}
        url = product_detail_url(product.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(product.ingredients.count(), 0)