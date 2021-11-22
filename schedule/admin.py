# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from schedule.models import Recipe, Meal, Ingredient

class RecipeInline(admin.TabularInline):
    model = Recipe
    fields = ('meal', 'ingredient', 'quantity')

class MealAdmin(admin.ModelAdmin):
    fields = ('name', 'cooking_time', 'tags', 'day_time', )
    inlines = [
        RecipeInline,
    ]

class IngredientAdmin(admin.ModelAdmin):
    fields = ('name',)

admin.site.register(Meal, MealAdmin)
admin.site.register(Ingredient, IngredientAdmin)

# Register your models here.
