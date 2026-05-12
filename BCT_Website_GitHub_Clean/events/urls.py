from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_event, name='create'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/edit/', views.edit_event, name='edit'),
    path('<int:pk>/delete/', views.delete_event, name='delete'),
    path('<int:pk>/rsvp/', views.rsvp, name='rsvp'),
]

