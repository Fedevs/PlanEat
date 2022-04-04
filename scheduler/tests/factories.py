import datetime

import factory.fuzzy

from scheduler.models import Category, Ingredient, Meal, Recipe, Schedule
from scheduler.tests.utils import get_ids_from_choices


DAY_TIME_CHOICE_IDS = get_ids_from_choices(Meal.DAY_TIME_CHOICES)
MEAL_TIME_CHOICE_IDS = get_ids_from_choices(Schedule.MEAL_TIME_CHOICES)
MEASUREMENT_UNIT_CHOICE_IDS = get_ids_from_choices(
    Ingredient.MEASUREMENT_UNIT_CHOICES
)
TAG_CHOICE_IDS = get_ids_from_choices(Meal.TAG_CHOICES)


class IngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ingredient

    name = factory.Faker('pystr', min_chars=5)
    measurement_unit = factory.fuzzy.FuzzyChoice(MEASUREMENT_UNIT_CHOICE_IDS)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('pystr', min_chars=5)
    frequency = factory.fuzzy.FuzzyInteger(0, 15)


class MealFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Meal

    name = factory.Faker('pystr', min_chars=5)
    tags = factory.fuzzy.FuzzyChoice(TAG_CHOICE_IDS)
    day_time = factory.fuzzy.FuzzyChoice(DAY_TIME_CHOICE_IDS)
    category = factory.SubFactory(CategoryFactory)
    yields = factory.fuzzy.FuzzyInteger(0, 10)
    cooking_time = factory.Faker('time_delta')
    enabled = factory.Faker('pybool')


class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recipe

    meal = factory.SubFactory(MealFactory)
    ingredient = factory.SubFactory(IngredientFactory)
    quantity = factory.fuzzy.FuzzyFloat(0, 1000)


class ScheduleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Schedule

    meal_time = factory.fuzzy.FuzzyChoice(MEAL_TIME_CHOICE_IDS)
    date = datetime.datetime.today()
    is_eaten = factory.Faker('pybool')
    meal = factory.SubFactory(MealFactory)
