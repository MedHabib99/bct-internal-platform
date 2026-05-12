from django import forms
from .models import Feedback, FeedbackReply

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["title", "category", "message", "attachment", "is_anonymous"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Short title"}),
            "message": forms.Textarea(attrs={"rows": 6, "placeholder": "Describe your feedback/issue…"}),
        }

class FeedbackReplyForm(forms.ModelForm):
    class Meta:
        model = FeedbackReply
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4, "placeholder": "Write your answer to the reporter…"}),
        }

class StatusUpdateForm(forms.Form):
    status = forms.ChoiceField(choices=Feedback.STATUS_CHOICES)
