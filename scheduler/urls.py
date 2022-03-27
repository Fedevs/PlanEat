from django.urls import path

from scheduler import views

urlpatterns = [
    path('', views.scheduler, name='scheduler'),
    path('lista_de_compras', views.ingredients_list, name='ingredients_list'),
    path('ingredient', views.ingredient, name='ingredient'),
    path('meal', views.meal, name='meal'),
]
