# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from schedule.models import Recipe, Meal, Ingredient, Category

class RecipeInline(admin.TabularInline):
    model = Recipe
    fields = ('meal', 'ingredient', 'quantity')
    raw_id_fields = ('ingredient',)


class MealAdmin(admin.ModelAdmin):
    fields = ('name', 'cooking_time', 'tags', 'day_time', 'category', )
    inlines = [
        RecipeInline,
    ]
    raw_id_fields = ('category',)


class CategoryAdmin(admin.ModelAdmin):
    fields = ('name',)


class IngredientAdmin(admin.ModelAdmin):
    fields = ('name', 'measurement_unit')
    search_fields = ('name',)


admin.site.register(Meal, MealAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Category, CategoryAdmin)

# Register your models here.
