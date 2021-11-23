from django.conf.urls import url
from . import views

urlpatterns = [
    url('', views.schedule, name='schedule'),
]