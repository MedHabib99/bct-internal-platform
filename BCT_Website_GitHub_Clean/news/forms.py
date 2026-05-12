from django import forms
from django.utils import timezone
from .models import NewsArticle, NewsCategory


class NewsForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = ['title', 'content', 'category', 'status', 'publish_date', 'is_important']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Article Title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Article Content',
                'rows': 10
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'publish_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'is_important': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        help_texts = {
            'publish_date': 'Leave empty to auto-set when publishing. Only relevant for published articles.',
            'status': 'Draft articles are only visible to teamleaders',
            'is_important': 'Important articles are pinned to the top of the list',
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        publish_date = cleaned_data.get('publish_date')

        if status == 'published' and not publish_date:
            cleaned_data['publish_date'] = timezone.now()

        if status == 'draft':
            cleaned_data['publish_date'] = None

        return cleaned_data
