"""
Script to recreate all deleted app files for BCT Website
Run this with: python create_remaining_files.py
"""

import os

# Define all file contents
FILES = {
    # PARTNERS APP
    'partners/__init__.py': '',
    'partners/apps.py': '''from django.apps import AppConfig


class PartnersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'partners'
''',
    'partners/models.py': '''from django.db import models

class Partner(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('restaurant', 'Restaurant'),
        ('attraction', 'Attraction'),
        ('hotel', 'Hotel'),
        ('transport', 'Transport'),
        ('other', 'Other'),
    ])
    address = models.CharField(max_length=300, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    discount_info = models.TextField(blank=True, help_text="Special discounts or offers for BCT")
    logo = models.ImageField(upload_to='partners/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
''',
    'partners/admin.py': '''from django.contrib import admin
from .models import Partner


def is_teamleader(user):
    return (
        user.is_authenticated and (
            user.is_superuser or
            user.groups.filter(name__iexact="TeamLeaders").exists()
        )
    )


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'phone', 'email']
    list_filter = ['category']
    search_fields = ['name', 'description', 'address']
    
    def has_module_permission(self, request):
        return is_teamleader(request.user)
    
    def has_add_permission(self, request):
        return is_teamleader(request.user)
    
    def has_change_permission(self, request, obj=None):
        return is_teamleader(request.user)
    
    def has_delete_permission(self, request, obj=None):
        return is_teamleader(request.user)
''',
    'partners/views.py': '''from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Partner

@login_required
def index(request):
    category = request.GET.get('category', '')
    
    if category:
        partners = Partner.objects.filter(category=category)
    else:
        partners = Partner.objects.all()
    
    context = {
        'partners': partners,
        'selected_category': category,
        'categories': Partner._meta.get_field('category').choices,
    }
    return render(request, 'partners/index.html', context)
''',
    'partners/urls.py': '''from django.urls import path
from . import views

app_name = 'partners'

urlpatterns = [
    path('', views.index, name='index'),
]
''',
    'partners/tests.py': '''from django.test import TestCase

# Create your tests here.
''',
    'partners/migrations/__init__.py': '',
}

# Create all files
print("Creating files...")
for filepath, content in FILES.items():
    # Create directory if needed
    dir_path = os.path.dirname(filepath)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"  Created directory: {dir_path}")
    
    # Write file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  ✓ {filepath}")

print("\n✅ All files created successfully!")
print("\nNext steps:")
print("1. Run: python create_news_events.py")
print("2. Update settings.py and urls.py")
print("3. Run migrations")

