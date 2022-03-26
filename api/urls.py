from django.urls import include, path
from rest_framework import routers

from api import views


router = routers.DefaultRouter()
router.register(r'ingredients', views.IngredientViewSet)
router.register(r'meals', views.MealViewSet)
router.register(r'recipes', views.RecipeViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'schedules', views.ScheduleViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]