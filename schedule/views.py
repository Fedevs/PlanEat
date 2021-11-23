from os import name
from django.shortcuts import render
from .models import Meal
from random import choice
# Create your views here.

def schedule(request):
    meals = {}
    meals["LN"] = list(Meal.objects.filter(day_time="LN"))
    meals["DN"] = list(Meal.objects.filter(day_time="DN"))
    meals["DL"] = list(Meal.objects.filter(day_time="DL"))

    days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    week = {}
    for day in days:
        week[day] = {"LN":"",
                     "DN": ""
                    }
    for day in week:
        for slot in week[day]:
            available_meals =  meals[slot] + meals['DL']
            #import ipdb; ipdb.set_trace()
            found = False
            meal = Meal() #esto puede fallar
            while(not found and available_meals!=[]):
                meal_temp = choice(available_meals)
                if meal_valid(slot, available_meals):
                    found = True
                    meal = meal_temp
                else:
                    available_meals.remove(meal_temp)

            if not found:
                print("no ṕudimos encontrar una comdia valida")
                break
            week[day][slot] = meal
            meals[meal.day_time].remove(meal)
    
    lunch = []
    dinner = []
    for food in week.values():
        for day_time, food in food.items():
            if day_time == "LN":
                lunch.append(food)
            else:
                dinner.append(food)
    
    final_meals = zip(lunch, dinner, week.keys())

    return render(request, 'ingredients.html', {'final_meals': final_meals, 'week': week, 'dinner_meals':dinner, 'lunch_meals':lunch, 'days': days})

def meal_valid(slot, available_meals):
    return True