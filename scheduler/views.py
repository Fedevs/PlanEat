from django.http import HttpRequest
from django.shortcuts import render, redirect


from .forms import IngredientForm, MealForm, RecipeFormSet, ScheduleForm, IngredientListForm
from .scheduler import (
    create_or_update_week_menu, get_current_menu, get_ingredients_needed
)


def scheduler(request):
    form = ScheduleForm()
    menu_changes = {}
    full_menu = {}

    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # now in the object cd, you have the form as a dictionary.
            start_date = cd.get('start_date')
            end_date = cd.get('end_date')

            menu_changes = create_or_update_week_menu(start_date, end_date)
            full_menu = get_current_menu(start_date, end_date)

    context = dict(
        menu_changes=menu_changes,
        full_menu=full_menu,
        form=form
    )

    return render(request, 'scheduler.html', context)


def ingredients_list(request):
    form = IngredientListForm()
    ingredients = {}
    full_menu = {}
    if request.method == 'POST':
        form = IngredientListForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # now in the object cd, you have the form as a dictionary.
            start_date = cd.get('start_date')
            end_date = cd.get('end_date')
            yields = cd.get('yields')
            full_menu = get_current_menu(start_date, end_date, yields)
            ingredients = get_ingredients_needed(full_menu)

    context = dict(
        full_menu=full_menu,
        ingredients=ingredients,
        form=form
    )
    return render(request, 'ingredients.html', context)


def meal(request):
    if request.method == 'POST':
        if 'add_ingredient' in request.POST:
            return _handle_fieldset_addition(request)
        return _handle_recipe_meal_creation(request)

    recipe_form = RecipeFormSet(prefix='recipe_form')
    meal_form = MealForm()

    return render(
        request=request,
        template_name='meal.html',
        context=dict(
            meal_form=meal_form,
            recipe_form=recipe_form,
        )
    )


def ingredient(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save()
            return redirect('ingredient')

    form = IngredientForm()
    return render(
        request=request,
        template_name='ingredient.html',
        context=dict(ingredient_form=form),
    )


def _handle_recipe_meal_creation(request):
    '''_handle_recipe_meal_creation handles the creation of a new meal.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpRequest: The request object.
    '''
    meal_form = MealForm(request.POST)
    if meal_form.is_valid():
        meal = meal_form.save()
        recipe_formset = RecipeFormSet(request.POST, prefix='recipe_form')
        if recipe_formset.is_valid():
            for recipe in recipe_formset:
                recipe.save(meal)
        return redirect('meal')


def _handle_fieldset_addition(request):
    '''_handle_fieldset_addition handles the addition of a new fieldset to the form.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpRequest: The request object.
    '''
    cp = request.POST.copy()
    cp['recipe_form-TOTAL_FORMS'] = int(cp['recipe_form-TOTAL_FORMS'])+ 1
    recipe_form = RecipeFormSet(cp,prefix='recipe_form')

    meal_form = MealForm(cp)
    context = dict(meal_form=meal_form, recipe_form=recipe_form)
    return render(
        request=request,
        template_name='meal.html',
        context=context,
    )
