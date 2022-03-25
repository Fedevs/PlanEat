import calendar
from datetime import date, timedelta

from django.db.models import Q

from .models import Meal, Schedule
# Create your views here.

def schedule():
    #TODO: revisar como empieza
    starting_date = date.today()
    current_date = starting_date
    menu =[]

    days = calendar.day_name
    for _ in days:
        if calendar.day_name[current_date.weekday()] == 'Monday':
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
            menu.append(new_meal_scheduled)

        current_date += timedelta(days=1)
    return menu

def meal_validity(meal: Meal, current_date, meal_time):
    previous_meals = Schedule.objects.filter(
        date__lte=current_date
    ).exclude(
        date=current_date, meal_time=meal_time
    ).order_by('-date', 'meal_time')
    meals_in_frequency = previous_meals[:meal.category.frequency]
    previous_categories = meals_in_frequency.values_list('meal__category__name', flat=True)

    return not meal.category.name in previous_categories
