# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from scheduler.models import Recipe, Meal, Ingredient, Category, Schedule


class RecipeInline(admin.StackedInline):
    model = Recipe
    fields = ('meal', 'ingredient', 'quantity')
    autocomplete_fields = ['ingredient']


class MealAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    inlines = [
        RecipeInline,
    ]
    autocomplete_fields = ['category']


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class ScheduleAdmin(admin.ModelAdmin):
    search_fields = ('meal__name',)
    list_filter = (
        'date',
        'meal_time',
        'meal__category',
    )
    list_display = (
        'date',
        'meal_time',
        'meal',
    )
    autocomplete_fields = ['meal']


admin.site.register(Meal, MealAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Schedule, ScheduleAdmin)
