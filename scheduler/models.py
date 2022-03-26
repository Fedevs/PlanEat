from django.db import models


class Ingredient(models.Model):
    MEASUREMENT_UNIT_CHOICES = [
        ('ml', 'Mililitro'),
        ('l', 'Litro'),
        ('mg', 'Miligramo'),
        ('g', 'Gramo'),
        ('kg', 'Kilogramo'),
        ('u', 'Unidad'),
    ]
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    measurement_unit = models.CharField(
        max_length=2,
        choices=MEASUREMENT_UNIT_CHOICES,
        default='g',
        verbose_name='Unidad de medida',
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Ingrediente'
        verbose_name_plural = 'Ingredientes'


class Meal(models.Model):
    DAY_TIME_CHOICES = [
        ('LN', 'Almuerzo'),
        ('DN', 'Cena'),
        ('DL', 'Almuerzo/Cena'),
    ]
    TAG_CHOICES = [
        ('OM', 'Omnívoro'),
        ('VT', 'Vegetariano'),
        ('VG', 'Vegano'),
    ]
    name = models.CharField(max_length=50, verbose_name='Nombre', unique=True)
    tags = models.CharField(
        max_length=2,
        choices=TAG_CHOICES,
        default='OM',
        verbose_name='Etiquetas',
    )
    day_time = models.CharField(
        max_length=2,
        choices=DAY_TIME_CHOICES,
        default='BR',
        verbose_name='Momento del día',
    )
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Categoria')
    enabled = models.BooleanField(default=True, verbose_name='Habilitada')
    cooking_time = models.DurationField(verbose_name='Tiempo de cocción', null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Comida'
        verbose_name_plural = 'Comidas'


class Recipe(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE,  verbose_name='Comida', related_name='recipes')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='recipes', verbose_name='Ingrediente')
    quantity = models.FloatField(verbose_name='Cantidad')

    def __str__(self) -> str:
        return f'{self.meal}'
    
    class Meta:
        verbose_name = 'Receta'
        verbose_name_plural = 'Recetas'


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Categoria', unique=True)
    frequency = models.PositiveIntegerField(verbose_name='Frecuencia')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'


class Schedule(models.Model):
    MEAL_TIME_CHOICES = [
        ('LN', 'Almuerzo'),
        ('DN', 'Cena'),
    ]
    meal_time = models.CharField(
        max_length=2,
        choices=MEAL_TIME_CHOICES,
        default='LN',
        verbose_name='Almuerzo/Cena',
    )
    date = models.DateField(verbose_name='Fecha')
    is_eaten = models.BooleanField(default=False, verbose_name='Consumida')
    meal = models.ForeignKey(
        'Meal', verbose_name='Comida', on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self) -> str:
        return f'{self.date} - {self.meal_time} - {self.meal}'

    class Meta:
        verbose_name = 'Menú'
        verbose_name_plural = 'Menús'
        unique_together = ['date', 'meal_time']
        ordering = ('date', '-meal_time',)
