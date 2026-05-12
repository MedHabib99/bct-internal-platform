from django.db import models
from django.conf import settings

class Document(models.Model):
    VISIBLE_ALL = "all"
    VISIBLE_TEAMLEAD = "teamleaders"
    VISIBILITY_CHOICES = [
        (VISIBLE_ALL, "All users"),
        (VISIBLE_TEAMLEAD, "Teamleaders only"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="documents/%Y/%m/")
    visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default=VISIBLE_ALL,
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_documents",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
