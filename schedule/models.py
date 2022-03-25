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
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre',)
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
        ('VG','Vegano'),
        ('VT','Vegetariano'),
        ('OM','Omnívoro'),
    ]
    name = models.CharField(max_length=50, verbose_name='Nombre')
    cooking_time = models.CharField(max_length=10, verbose_name='Tiempo de cocción')
    tags = models.CharField(
        max_length=2,
        choices=TAG_CHOICES,
        default='',
        verbose_name='Etiquetas',
    )
    day_time = models.CharField(
        max_length=2,
        choices=DAY_TIME_CHOICES,
        default='BR',
        verbose_name='Momento del día',
    )
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Comida'
        verbose_name_plural = 'Comidas'


class Recipe(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE,  verbose_name='Comida')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='Ingredients', verbose_name='Ingrediente')
    quantity =   models.FloatField(verbose_name='Cantidad')

    def __str__(self) -> str:
        return self.meal
    
    class Meta:
        verbose_name = 'Receta'
        verbose_name_plural = 'Recetas'


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Categoría')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorias'
