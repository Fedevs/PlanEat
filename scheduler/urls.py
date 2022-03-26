from django.urls import path

from schedule import views

urlpatterns = [
    path('', views.scheduler, name='scheduler'),
    path('ingredient', views.ingredient, name='ingredient'),
    path('meal', views.meal, name='meal'),
]
