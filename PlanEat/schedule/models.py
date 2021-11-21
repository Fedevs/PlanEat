from django.db import models

class Meals(models.model):
    KIND_CHOICES = [
        ('meat', 'Con carne'),
        ('vegan', 'Vegana'),
        ('veggie', 'vegetariana'),
    ]
    DAY_TIME_CHOICES = [
        ('BR', 'Desayuno'),
        ('LN', 'Almuerzo'),
        ('TT', 'Merienda'),
        ('DN', 'Cena'),
        ('DL', 'Almuerzo/Cena'),
        ('BT', 'Desayuno/Merienda'),
    ]
    name = models.CharField(max_length=50, verbose_name='Nombre')
    ingredients = models.ManyToManyField(Ingredients, verbose_name='Ingredientes')
    cooking_time = models.CharField(max_length=10, verbose_name='Tiempo de cocción')
    kind = models.CharField(
        choices=KIND_CHOICES,
        default='vegan',
        verbose_name='Tipo de comida',
    )
    day_time = models.CharField(
        choices=DAY_TIME_CHOICES,
        default='BR',
        verbose_name='Momento del día',
    )
    recipe = models.CharField(null=True, blank=True, verbose_name='Receta')


class Ingredients(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre'),
    meals = models.ForeignKey(Meals, on_delete=models.CASCADE),
    quantity = models.IntegerField(verbose_name='Cantidad')