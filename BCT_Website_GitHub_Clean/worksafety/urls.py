from django.urls import path
from . import views

app_name = 'worksafety'

urlpatterns = [
    # Main page
    path('', views.index, name='index'),
    
    # Document views
    path('documents/<int:pk>/', views.document_detail, name='document_detail'),
    path('documents/<int:pk>/acknowledge/', views.acknowledge_document, name='acknowledge_document'),
    
    # Team Leader - Document management
    path('documents/create/', views.create_document, name='create_document'),
    path('documents/<int:pk>/edit/', views.edit_document, name='edit_document'),
    path('documents/<int:pk>/delete/', views.delete_document, name='delete_document'),
    
    # Team Leader - Category management
    path('categories/', views.manage_categories, name='manage_categories'),
    path('categories/create/', views.create_category, name='create_category'),
    path('categories/<int:pk>/edit/', views.edit_category, name='edit_category'),
    path('categories/<int:pk>/delete/', views.delete_category, name='delete_category'),
    
    # Team Leader - Emergency info management
    path('emergency/edit/', views.edit_emergency_info, name='edit_emergency_info'),
    
    # Incident reporting
    path('incident/report/', views.report_incident, name='report_incident'),
    path('incidents/', views.list_incidents, name='list_incidents'),
    path('incidents/<int:pk>/', views.incident_detail, name='incident_detail'),
]

