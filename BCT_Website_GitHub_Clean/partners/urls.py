from django.urls import path
from . import views

app_name = 'partners'

urlpatterns = [
    path('', views.index, name='index'),
]

