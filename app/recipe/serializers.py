"""
Serializers for the recipe API view.
"""


from django.utils.translation import gettext as _
from rest_framework import serializers
from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""

    class Meta:
        model = Recipe
        field = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']