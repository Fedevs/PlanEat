from django.urls import path
from schedule import views

urlpatterns = [
    path('', views.schedule, name='schedule'),
    path('ingredient', views.ingredient, name='ingredient'),
    path('meal', views.meal, name='meal'),
]