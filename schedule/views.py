from django.shortcuts import render
from .models import Ingredient

# Create your views here.

def schedule(request):
    days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    ingredients = Ingredient.objects.all()
    return render(request, 'ingredients.html', {'ingredients': ingredients, 'days': days})
