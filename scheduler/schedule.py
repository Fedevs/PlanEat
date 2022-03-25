from os import name
import calendar
from django.shortcuts import render
from .models import Meal, Schedule
from random import choice, random
from datetime import date, timedelta
# Create your views here.

def schedule(request):
    
    lunch_meals = Meal.objects.exclude(day_time="DN").order_by("?")
    dinner_meals = Meal.objects.exclude(day_time="LN").order_by("?")
    
    #TODO: revisar como empieza
    starting_date = date.today()
    menu =[]

    days = calendar.day_name
    for day in days:
        #For lunch
        lunch_meal = None
        for meal in lunch_meals.iterator():
            if meal_validity(meal):
                lunch_meal = meal
                break
        schedule_ln = Schedule.objects.create(date=starting_date, meal_time="LN", meal=lunch_meal)
        menu.append(schedule_ln)
        dinner_meal = None
        #For dinner 
        for meal in dinner_meal.iterator():
            if meal_validity(meal):
                dinner_meal = meal
                break
        schedule_dn = Schedule.objects.create(date=starting_date, meal_time="DN", meal=dinner_meal)
        menu.append(schedule_dn)
        starting_date+= timedelta(days=1)

    return menu

def meal_validity(meal):
    return True