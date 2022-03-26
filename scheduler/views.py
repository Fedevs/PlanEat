from os import name

from django.shortcuts import render

from .schedule import (
    create_or_update_week_menu, get_current_menu, get_ingredients_needed
)


def scheduler(request):
    menu_changes = create_or_update_week_menu()
    full_menu = get_current_menu()
    ingredients = get_ingredients_needed(full_menu)

    context = dict(
        menu_changes=menu_changes,
        full_menu=full_menu,
        ingredients=ingredients,
    )
    return render(request, 'ingredients.html', context)
