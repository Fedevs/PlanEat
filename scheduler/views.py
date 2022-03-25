from os import name
from django.shortcuts import render
from .schedule import schedule
# Create your views here.

def scheduler(request):
    menu = schedule()

    return render(request, 'ingredients.html', {"menu": menu, "ingredients": []})

