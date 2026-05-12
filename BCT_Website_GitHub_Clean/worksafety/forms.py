from django import forms
from .models import (
    WorkSafetyDocument,
    WorkSafetyCategory,
    WorkSafetyEmergencyInfo,
    WorkSafetyIncidentReport
)


class WorkSafetyDocumentForm(forms.ModelForm):
    class Meta:
        model = WorkSafetyDocument
        fields = ['title', 'description', 'category', 'file', 'version', 'status', 'visible_to']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Document Title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Brief description of this document',
                'rows': 3
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'version': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 1.0, 1.1, 2.0'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'visible_to': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        help_texts = {
            'version': 'Update version when making significant changes (users will need to re-acknowledge)',
            'status': 'Only active documents are visible to users',
            'visible_to': 'Control who can view this document',
            'file': 'Upload PDF, Word, or other document formats'
        }

    def clean_version(self):
        version = self.cleaned_data.get('version')
        if not version:
            raise forms.ValidationError("Version is required")
        if not any(char.isdigit() for char in version):
            raise forms.ValidationError("Version should contain at least one number (e.g. 1.0)")
        return version


class WorkSafetyCategoryForm(forms.ModelForm):
    class Meta:
        model = WorkSafetyCategory
        fields = ['name', 'slug', 'order']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Category Name'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'category-slug'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0'
            }),
        }
        help_texts = {
            'slug': 'URL-friendly name (lowercase, hyphens only)',
            'order': 'Display order (lower numbers appear first)'
        }


class WorkSafetyEmergencyInfoForm(forms.ModelForm):
    class Meta:
        model = WorkSafetyEmergencyInfo
        fields = ['emergency_number', 'police_number', 'company_contact_name', 'company_contact_phone', 'quick_steps']
        widgets = {
            'emergency_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '112'
            }),
            'police_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '110'
            }),
            'company_contact_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Emergency Contact Name'
            }),
            'company_contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+49 123 456 789'
            }),
            'quick_steps': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '1. Stay calm\n2. Call emergency services\n3. Secure the area\n4. Provide first aid if trained\n5. Document the incident',
                'rows': 6
            }),
        }
        help_texts = {
            'quick_steps': 'Enter 3-6 quick action steps (one per line)'
        }


class WorkSafetyIncidentReportForm(forms.ModelForm):
    class Meta:
        model = WorkSafetyIncidentReport
        fields = ['title', 'description', 'location', 'occurred_at']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief title of the incident'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe what happened in detail...',
                'rows': 6
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Where did this occur? (building, floor, room, etc.)'
            }),
            'occurred_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }
        help_texts = {
            'description': 'Provide as much detail as possible about what happened',
            'occurred_at': 'When did this incident occur?'
        }


class IncidentStatusForm(forms.ModelForm):
    class Meta:
        model = WorkSafetyIncidentReport
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
