from os import name

from django.shortcuts import render
from .schedule import schedule

def scheduler(request):
    menu = schedule()

    return render(request, 'ingredients.html', {"menu": menu, "ingredients": []})

