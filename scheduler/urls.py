from django.urls import path

from scheduler import views

urlpatterns = [
    path('', views.scheduler, name='scheduler'),
    path(
        'listado-de-compras', views.ingredients_list, name='ingredients_list'
    ),
    path('ingredient', views.ingredient, name='ingredient'),
    path('meal', views.meal, name='meal'),
]
