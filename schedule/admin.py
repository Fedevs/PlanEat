# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from schedule.models import Recipe, Meal, Ingredient, Category, Schedule


class RecipeInline(admin.TabularInline):
    model = Recipe
    fields = ('meal', 'ingredient', 'quantity')


class MealAdmin(admin.ModelAdmin):
    inlines = [
        RecipeInline,
    ]


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class ScheduleAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    filter_fields = ('date', 'meal_time',)


admin.site.register(Meal, MealAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Schedule, ScheduleAdmin)

# Register your models here.
