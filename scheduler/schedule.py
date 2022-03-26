import calendar
from datetime import date, timedelta

from django.db.models import Q

from .models import Meal, Schedule


def create_or_update_week_menu():
    days = calendar.day_name
    starting_date = date.today()
    current_date = starting_date
    menu_changes = []

    for _ in days:
        if days[current_date.weekday()] == 'Monday':
            break

        for meal_time in ['LN', 'DN']:
            if Schedule.objects.filter(
                date=current_date, meal_time=meal_time, meal__isnull=False
            ).exists():
                continue

            meal = None
            candidate_meals = Meal.objects.filter(
                Q(day_time=meal_time) | Q(day_time='DL')
            ).order_by('?')

            for candidate_meal in candidate_meals.iterator():
                if meal_validity(candidate_meal, current_date, meal_time):
                    meal = candidate_meal
                    break

            new_meal_scheduled, _ = Schedule.objects.update_or_create(
                date=current_date, meal_time=meal_time, defaults={"meal": meal}
            )
            menu_changes.append(new_meal_scheduled)

        current_date += timedelta(days=1)
    return menu_changes


def meal_validity(meal: Meal, current_date, meal_time):
    previous_meals = Schedule.objects.filter(
        date__lte=current_date
    ).exclude(
        date=current_date, meal_time=meal_time
    ).order_by('-date', 'meal_time')
    meals_in_frequency = previous_meals[:meal.category.frequency]
    previous_categories = meals_in_frequency.values_list('meal__category__name', flat=True)

    return not meal.category.name in previous_categories


def get_last_monday():
    days = calendar.day_name
    today = date.today()

    last_monday = today - timedelta(days=today.weekday())

    return last_monday


def get_current_menu():
    last_monday = get_last_monday()
    menu = Schedule.objects.filter(date__gte=last_monday)

    return menu


def get_ingredients_needed(menu):
    ingredients = {}

    for schedule in menu.iterator():
        if schedule.meal is not None:
            recipes = schedule.meal.recipes.all()       
            for recipe in recipes.iterator():
                ingredient = recipe.ingredient

                if ingredient.name not in ingredients.keys():
                    ingredients[ingredient.name] = {
                        'quantity': 0,
                        'unit': ingredient.measurement_unit,
                    }
                
                ingredients[ingredient.name]['quantity'] += recipe.quantity            
    return ingredients
