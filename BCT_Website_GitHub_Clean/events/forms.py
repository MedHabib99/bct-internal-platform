from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'max_participants', 'participants_visible_to']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Event Title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Event Description',
                'rows': 5
            }),
            'date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Event Location'
            }),
            'max_participants': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Leave empty for unlimited',
                'min': 1
            }),
            'participants_visible_to': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        help_texts = {
            'max_participants': 'Leave empty for unlimited participants',
            'participants_visible_to': 'Choose who can see the list of participants'
        }
