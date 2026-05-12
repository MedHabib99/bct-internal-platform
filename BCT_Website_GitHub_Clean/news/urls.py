from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_news, name='create'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/edit/', views.edit_news, name='edit'),
    path('<int:pk>/delete/', views.delete_news, name='delete'),
]

