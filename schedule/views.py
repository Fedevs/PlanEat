from os import name
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from schedule.forms import IngredientForm, MealForm, RecipeForm, RecipeFormSet
from .models import Ingredient, Meal, Recipe
from random import choice
# Create your views here.

def meal(request):
    FormSet = inlineformset_factory(Meal, Recipe, can_delete=False, form=RecipeForm, extra=1)
    if request.method == 'POST':
        
        if 'add' in request.POST:
            print(request.POST)
            cp = request.POST.copy()
            cp['recipe_form-TOTAL_FORMS'] = int(cp['recipe_form-TOTAL_FORMS'])+ 1
            recipe_form = FormSet(cp,prefix='recipe_form')

            meal_form = MealForm(cp)
            return render(request=request, template_name="meal.html", context={"meal_form":meal_form, "recipe_form":recipe_form})
        meal_form = MealForm(request.POST)
        if meal_form.is_valid():
            meal = meal_form.save()
            recipe_formset = FormSet(request.POST, prefix='recipe_form')
            if recipe_formset.is_valid():
                for recipe in recipe_formset:
                    recipe.save(meal)
            return redirect("meal")
    recipe_form = FormSet(prefix='recipe_form')
    meal_form = MealForm()
    
    return render(request=request, template_name="meal.html", context={"meal_form":meal_form, "recipe_form":recipe_form})

def ingredient(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save()
            return redirect("ingredient")
    form = IngredientForm()
    return render(request=request, template_name="ingredient.html", context={"ingredient_form":form})

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