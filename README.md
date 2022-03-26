# PlanEat

Planificador de comidas semanales

## Instalación

Crear venv (como mas te guste)


Instalar los requerimientos

`pip install -r requirements.txt`


Correr migraciones:

`python manage.py migrate`


Crear un superusario para acceder al admin:

`python manage.py createsuperuser`


Cargar datos iniciales:

`python manage.py loaddata schedule/fixtures/init_data.json` 


Iniciar el servidor:

`python manage.py runserver`
