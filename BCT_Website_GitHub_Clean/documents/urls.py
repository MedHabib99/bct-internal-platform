# documents/urls.py
from django.urls import path
from .views import DocumentListView, DocumentCreateView, DocumentUpdateView, DocumentDeleteView

app_name = "documents"

urlpatterns = [
    path("", DocumentListView.as_view(), name="index"),
    path("upload/", DocumentCreateView.as_view(), name="upload"),
]

#Modify/Delete
urlpatterns = [
    path("", DocumentListView.as_view(), name="index"),
    path("upload/", DocumentCreateView.as_view(), name="upload"),
    path("<int:pk>/edit/", DocumentUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", DocumentDeleteView.as_view(), name="delete"),
]
