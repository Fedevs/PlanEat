import pytest

from scheduler.models import Schedule
from scheduler.scheduler import get_ingredients_needed
from scheduler.tests.factories import (
    IngredientFactory,
    MealFactory,
    RecipeFactory,
    ScheduleFactory,
)


@pytest.mark.django_db
def test_get_ingredients_needed_default():
    onion = IngredientFactory(name='Onion', measurement_unit='u')
    tomato = IngredientFactory(name='Tomato', measurement_unit='u')
    lettuce = IngredientFactory(name='Lettuce', measurement_unit='u')
    oil = IngredientFactory(name='Oil', measurement_unit='ml')

    mixed_salad = MealFactory(
        name='Mixed Salad', tags='VG', day_time='DL', yields=1
    )

    RecipeFactory(meal=mixed_salad, ingredient=onion, quantity=0.5)
    RecipeFactory(meal=mixed_salad, ingredient=tomato, quantity=1)
    RecipeFactory(meal=mixed_salad, ingredient=lettuce, quantity=1)
    RecipeFactory(meal=mixed_salad, ingredient=oil, quantity=10)

    ScheduleFactory(meal=mixed_salad)

    ingredients = get_ingredients_needed(Schedule.objects.all())

    # Onion
    assert ingredients[onion.name]['unit'] == onion.measurement_unit
    assert ingredients[onion.name]['quantity'] == 0.5

    # Tomato
    assert ingredients[tomato.name]['unit'] == tomato.measurement_unit
    assert ingredients[tomato.name]['quantity'] == 1

    # Lettuce
    assert ingredients[lettuce.name]['unit'] == lettuce.measurement_unit
    assert ingredients[lettuce.name]['quantity'] == 1

    # Oil
    assert ingredients[oil.name]['unit'] == oil.measurement_unit
    assert ingredients[oil.name]['quantity'] == 10


@pytest.mark.django_db
def test_get_ingredients_needed_two_yields():
    onion = IngredientFactory(name='Onion', measurement_unit='u')
    tomato = IngredientFactory(name='Tomato', measurement_unit='u')
    lettuce = IngredientFactory(name='Lettuce', measurement_unit='u')
    oil = IngredientFactory(name='Oil', measurement_unit='ml')

    mixed_salad = MealFactory(
        name='Mixed Salad', tags='VG', day_time='DL', yields=1
    )

    RecipeFactory(meal=mixed_salad, ingredient=onion, quantity=0.5)
    RecipeFactory(meal=mixed_salad, ingredient=tomato, quantity=1)
    RecipeFactory(meal=mixed_salad, ingredient=lettuce, quantity=1)
    RecipeFactory(meal=mixed_salad, ingredient=oil, quantity=10)

    ScheduleFactory(meal=mixed_salad)

    ingredients = get_ingredients_needed(Schedule.objects.all(), yields=2)

    # Onion
    assert ingredients[onion.name]['unit'] == onion.measurement_unit
    assert ingredients[onion.name]['quantity'] == 1

    # Tomato
    assert ingredients[tomato.name]['unit'] == tomato.measurement_unit
    assert ingredients[tomato.name]['quantity'] == 2

    # Lettuce
    assert ingredients[lettuce.name]['unit'] == lettuce.measurement_unit
    assert ingredients[lettuce.name]['quantity'] == 2

    # Oil
    assert ingredients[oil.name]['unit'] == oil.measurement_unit
    assert ingredients[oil.name]['quantity'] == 20


@pytest.mark.django_db
def test_get_ingredients_needed_repeated_ingredients():
    onion = IngredientFactory(name='Onion', measurement_unit='u')
    tomato = IngredientFactory(name='Tomato', measurement_unit='u')
    lettuce = IngredientFactory(name='Lettuce', measurement_unit='u')
    oil = IngredientFactory(name='Oil', measurement_unit='ml')

    mixed_salad = MealFactory(
        name='Mixed Salad', tags='VG', day_time='DL', yields=1
    )
    simple_salad = MealFactory(
        name='Simple Salad', tags='VG', day_time='DL', yields=1
    )

    RecipeFactory(meal=mixed_salad, ingredient=onion, quantity=0.5)
    RecipeFactory(meal=mixed_salad, ingredient=tomato, quantity=1)
    RecipeFactory(meal=mixed_salad, ingredient=lettuce, quantity=1)
    RecipeFactory(meal=mixed_salad, ingredient=oil, quantity=10)
    RecipeFactory(meal=simple_salad, ingredient=tomato, quantity=1)
    RecipeFactory(meal=simple_salad, ingredient=lettuce, quantity=1)
    RecipeFactory(meal=simple_salad, ingredient=oil, quantity=10)

    ScheduleFactory(meal=mixed_salad, meal_time='LN')
    ScheduleFactory(meal=simple_salad, meal_time='DN')

    ingredients = get_ingredients_needed(Schedule.objects.all())

    # Onion
    assert ingredients[onion.name]['unit'] == onion.measurement_unit
    assert ingredients[onion.name]['quantity'] == 0.5

    # Tomato
    assert ingredients[tomato.name]['unit'] == tomato.measurement_unit
    assert ingredients[tomato.name]['quantity'] == 2

    # Lettuce
    assert ingredients[lettuce.name]['unit'] == lettuce.measurement_unit
    assert ingredients[lettuce.name]['quantity'] == 2

    # Oil
    assert ingredients[oil.name]['unit'] == oil.measurement_unit
    assert ingredients[oil.name]['quantity'] == 20


@pytest.mark.django_db
def test_get_ingredients_needed_schedule_empty():
    ScheduleFactory(meal=None)

    ingredients = get_ingredients_needed(Schedule.objects.all())

    assert len(ingredients.keys()) == 0


@pytest.mark.django_db
def test_get_ingredients_needed_three_yields_when_meal_with_yields():
    onion = IngredientFactory(name='Onion', measurement_unit='u')
    tomato = IngredientFactory(name='Tomato', measurement_unit='u')
    lettuce = IngredientFactory(name='Lettuce', measurement_unit='u')
    oil = IngredientFactory(name='Oil', measurement_unit='ml')

    mixed_salad = MealFactory(
        name='Mixed Salad', tags='VG', day_time='DL', yields=2
    )

    RecipeFactory(meal=mixed_salad, ingredient=onion, quantity=1)
    RecipeFactory(meal=mixed_salad, ingredient=tomato, quantity=2)
    RecipeFactory(meal=mixed_salad, ingredient=lettuce, quantity=2)
    RecipeFactory(meal=mixed_salad, ingredient=oil, quantity=20)

    ScheduleFactory(meal=mixed_salad)

    ingredients = get_ingredients_needed(Schedule.objects.all(), yields=3)

    # Onion
    assert ingredients[onion.name]['unit'] == onion.measurement_unit
    assert ingredients[onion.name]['quantity'] == 1.5

    # Tomato
    assert ingredients[tomato.name]['unit'] == tomato.measurement_unit
    assert ingredients[tomato.name]['quantity'] == 3

    # Lettuce
    assert ingredients[lettuce.name]['unit'] == lettuce.measurement_unit
    assert ingredients[lettuce.name]['quantity'] == 3

    # Oil
    assert ingredients[oil.name]['unit'] == oil.measurement_unit
    assert ingredients[oil.name]['quantity'] == 30
