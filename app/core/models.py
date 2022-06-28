"""
Database models
"""
from pydoc import describe
from django.conf import settings
from django.db import models
from django.contrib.auth.models import ( AbstractBaseUser, BaseUserManager, PermissionsMixin,)


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

class Product(models.Model):
    """Product object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    stock = models.IntegerField(default=0)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    availability = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    ingridients = models.ManyToManyField('Ingredient',blank=True)
    size = models.ManyToManyField('Size',blank=True)
    category = models.ManyToManyField('Category',blank=True)

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


class Ingredient(models.Model):
    """Ingredient object"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Size(models.Model):
    """Size object"""
    name = models.CharField(max_length=255)
    product_Type = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    amount_Unit = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return self.name


class Category(models.Model):
    """Catagory object"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name