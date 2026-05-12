from django.urls import path
from .views import (
    ContactGridView, ContactCreateView, ContactUpdateView, ContactDeleteView
)

app_name = "contacts"

urlpatterns = [
    path("", ContactGridView.as_view(), name="index"),
    path("add/", ContactCreateView.as_view(), name="add"),
    path("<int:pk>/edit/", ContactUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", ContactDeleteView.as_view(), name="delete"),
]