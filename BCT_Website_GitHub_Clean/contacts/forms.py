from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            "name", "title", "email", "whatsapp", "photo",
            "seller_of_month_count", "icebar_of_month_count",
            "joined_on",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Full name"}),
            "title": forms.TextInput(attrs={"placeholder": "Role / Title"}),
            "email": forms.EmailInput(attrs={"placeholder": "name@company.com"}),
            "whatsapp": forms.TextInput(attrs={"placeholder": "+216 12 345 678"}),
            "joined_on": forms.DateInput(attrs={"type": "date"}),
        }
