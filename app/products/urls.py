"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from products import views

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('tags', views.TagViewSet)
router.register('sizes', views.SizeViewSet)
router.register('ingredients', views.IngredientViewSet)
router.register('categories', views.CategoryViewSet)
router.register('categories', views.ManufacturerViewSet)



app_name = 'products'

urlpatterns = [
    path('', include(router.urls)),
]
