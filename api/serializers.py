from rest_framework import serializers

from scheduler.models import Ingredient, Meal, Recipe, Category, Schedule


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name', 'measurement_unit']


class MealSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Meal
        fields = [
            'name',
            'tags',
            'day_time',
            'category',
            'enabled',
            'cooking_time',
        ]


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'meal',
            'ingredient',
            'quantity',
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'name',
            'frequency',
        ]


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Schedule
        fields = ['meal_time', 'date', 'is_eaten', 'meal']
