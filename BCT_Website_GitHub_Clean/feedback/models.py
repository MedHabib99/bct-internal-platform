import uuid
from django.conf import settings
from django.db import models

class Feedback(models.Model):
    CATEGORY_CHOICES = [
        ("general", "General"),
        ("complaint", "Complaint"),
        ("it", "IT / Security"),
        ("hr", "HR / Schedule"),
        ("management", "Management"),
        ("other", "Other"),
    ]
    STATUS_CHOICES = [
        ("open", "Open"),
        ("ongoing", "Ongoing"),
        ("investigating", "Investigating"),
        ("forwarded", "Forwarded"),
        ("closed", "Closed"),
    ]

    title = models.CharField(max_length=150)
    category = models.CharField(max_length=24, choices=CATEGORY_CHOICES, default="general")
    message = models.TextField()
    attachment = models.FileField(upload_to="feedback/", blank=True, null=True)

    is_anonymous = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="feedbacks"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    created_at = models.DateTimeField(auto_now_add=True)

    tracker = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        ordering = ["-created_at"]

    def reporter_display(self):
        return "Anonymous" if self.is_anonymous or not self.created_by else self.created_by.get_username()

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


class FeedbackReply(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name="replies")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        who = self.author.get_username() if self.author else "TeamLeader"
        return f"Reply by {who} on {self.created_at:%Y-%m-%d %H:%M}"
