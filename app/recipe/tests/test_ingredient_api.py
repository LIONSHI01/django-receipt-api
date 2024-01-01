"""
Tests for ingredients API.
"""
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


def detail_url(ingredient_id):
    """Create and return an ingredient detail URL."""
    return reverse('recipe:ingredient-detail', args=[ingredient_id])


def create_user(email='user@@example.com', password='testpass1223'):
    return get_user_model().objects.create_user(email=email,
                                                password=password)


def create_ingredient(user, **params):
    """Create and return a sample ingredient."""
    defaults = {
        'name': 'Sample ingredient'
    }
    defaults.update(params)
    ingredient = Ingredient.objects.create(user=user, **defaults)
    return ingredient


class PublicIngredientsApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving ingredients."""
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """Test retrieving a list of ingredients."""
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Vanilla')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test list of ingredients is limited to authenticated user."""
        user2 = create_user(email='user2@example.com')
        Ingredient.objects.create(user=user2, name='Salt')
        ingredient = Ingredient.objects.create(user=self.user, name='Pepper')

        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0]['name'], ingredient.name)
        self.assertEqual(res.data[0]['id'], ingredient.id)

    def test_update_ingredient(self):
        """Test updating an ingredient."""
        ingredient = Ingredient.objects.create(user=self.user, name='Cilantro')

        # Update
        payload = {'name': 'Coriander'}

        # Assert http call ok
        url = detail_url(ingredient.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # Assert recipe ingredient name = payload name
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])

    def test_delete_ingredient(self):
        """Test deleting ingredient."""
        # create ingredient
        ingredient = Ingredient.objects.create(user=self.user, name='Lettuce')
        # delete ingredient
        url = detail_url(ingredient.id)
        res = self.client.delete(url)
        # assert response = 204
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        # assert ingredient not exist
        ingredients = Ingredient.objects.filter(user=self.user)
        self.assertFalse(ingredients.exists())