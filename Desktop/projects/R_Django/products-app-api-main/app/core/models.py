"""
Database models
"""
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import ( AbstractBaseUser, BaseUserManager, PermissionsMixin,)


def product_image_file_path(instance, filename):
    """Generate file path for new product image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'products', filename)


class UserManager(BaseUserManager):
    """Manager for user"""

    def create_user(self,email,password=None, **extra_field):
        """Create, save and return a new user"""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


UNIT_CHOICES = (
    ('kg', 'Kilograms'),
    ('lb', 'Pounds'),
    ('g', 'Grams'),
    ('oz', 'Ounces'),
    ('l', 'Liters'),
    ('ml', 'Milliliters'),
    ('gal', 'Gallons'),
    ('qt', 'Quarts'),
    ('fl oz', 'Fluid Ounces'),
    ('cup', 'Cups'),
)

SIZE_CHOICES = (
    ('XS', 'Extra Small'),
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Extra Large'),
    ('XXL', 'Double Extra Large'),
)

AVAILABLE_CHOICES = (
    ('In Stock', 'In Stock'),
    ('Out of Stock', 'Out of Stock'),
    ('Pre-Order', 'Pre-Order'),
)

AISLE_CHOICES = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E'),
    ('F', 'F'),
    ('G', 'G'),
    )

RACK_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
)

CATEGORIES_CHOICES = (
    ('Food', 'Food'),
    ('Drink', 'Drink'),
    ('Snack', 'Snack'),
    ('Dessert', 'Dessert'),
    ('Other', 'Other'),
)

DETAILED_CATEGORIES_CHOICES = (
('Other', 'Other'),
('Baby', 'Baby'),
('Beer, Wine & Spirits', 'Beer, Wine & Spirits'),
('Beverages:  tea, coffee, soda, juice, Kool-Aid, hot chocolate, water, etc.', 'Beverages:  tea, coffee, soda, juice, Kool-Aid, hot chocolate, water, etc.'),
('Bread & Bakery', 'Bread & Bakery'),
('Breakfast & Cereal', 'Breakfast & Cereal'),
('Canned Goods & Soups', 'Canned Goods & Soups'),
('Condiments/Spices & Bake', 'Condiments/Spices & Bake'),
('Cookies, Snacks & Candy', 'Cookies, Snacks & Candy'),
('Dairy, Eggs & Cheese', 'Dairy, Eggs & Cheese'),
('Deli & Signature Cafe', 'Deli & Signature Cafe'),
('Flowers & Plants', 'Flowers & Plants'),
('Frozen Foods', 'Frozen Foods'),
('Produce: Fruits & Vegetables', 'Produce: Fruits & Vegetables'),
('Grains, Pasta & Sides', 'Grains, Pasta & Sides'),
('International Cuisine', 'International Cuisine'),
('Meat & Seafood', 'Meat & Seafood'),
('Miscellaneous: gift cards/wrap, batteries, etc.', 'Miscellaneous: gift cards/wrap, batteries, etc.'),
('Paper Products toilet paper, paper towels, tissues, paper plates/cups, etc.', 'Paper Products: toilet paper, paper towels, tissues, paper plates/cups, etc.'),
('Cleaning Supplies: laundry detergent, dishwashing soap, etc.', 'Cleaning Supplies : laundry detergent, dishwashing soap, etc.'),
('Health & Beauty, Personal Care & Pharmacy: pharmacy items, shampoo, toothpaste', 'Health & Beauty, Personal Care & Pharmacy : pharmacy items, shampoo, toothpaste'),
('Pet Care', 'Pet Care'),
('Pharmacy', 'Pharmacy'),
('Tobacco', 'Tobacco'),
)

class Product(models.Model):
    """Product object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    image = models.ImageField(null=True, upload_to=product_image_file_path)
    brand = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    aisle = models.CharField(max_length=255, choices=AISLE_CHOICES, default='A')
    rack_number = models.CharField(choices=RACK_CHOICES, default='1', max_length=10)
    size = models.CharField(max_length=255, choices = SIZE_CHOICES,default = 'small')
    stock = models.IntegerField(default=0)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    unit = models.CharField(max_length = 20,choices=UNIT_CHOICES, default = 'oz')
    availability = models.CharField(max_length = 20,choices=AVAILABLE_CHOICES, default = 'In Stock')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=255, choices=CATEGORIES_CHOICES, default='Food')
    sub_category = models.CharField(max_length=255, choices=DETAILED_CATEGORIES_CHOICES, default='None')
    tags = models.ManyToManyField('Tag', blank=True)
    manufacturer = models.ManyToManyField('Manufacturer', blank=False)

    def __str__(self):
        return self.name

class Tag(models.Model):
    """Tag object"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    """Manufacturer name"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name