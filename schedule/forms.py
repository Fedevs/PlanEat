from distutils.command.clean import clean
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Row, Column
from schedule.models import Ingredient, Meal, Recipe

class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = ['name', 'measurement_unit']

    def save(self, commit=True):
        ingredient = super(IngredientForm, self).save(commit=False)

        if commit:
            ingredient.save()
        return ingredient

class MealForm(forms.ModelForm):

    class Meta:
        model = Meal
        fields = ['name', 'cooking_time', 'tags', 'day_time', 'category']
    
    def __init__(self, *args, **kwargs):
        super(MealForm, self).__init__(*args, **kwargs)
        self.fields['category'].required = False
    
    def save(self, commit=True):
        meal = super(MealForm, self).save(commit=False)

        if commit:
            meal.save()
        return meal

class RecipeForm(forms.ModelForm):


    class Meta:
        model = Recipe
        fields = ['ingredient', 'quantity']
        widgets = {
            'ingredient': forms.Select(attrs={'class': 'form-control ingredient'}),
            'quantity': forms.TextInput(attrs={'class': 'form-control quant'}),
        }
    
    def save(self, meal, commit=True):

        cleaned_data = self.cleaned_data

        cleaned_data.pop('id')
        cleaned_data['meal'] = meal

        if commit:
            recipe = Recipe.objects.create(**cleaned_data)
            return recipe
        
        return None


    
RecipeFormSet = forms.inlineformset_factory(Meal, Recipe, fields=('ingredient', 'quantity'), extra=1)