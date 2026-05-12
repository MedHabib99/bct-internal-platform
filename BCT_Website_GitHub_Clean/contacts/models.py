from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=120)
    title = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    whatsapp = models.CharField(max_length=30, blank=True, help_text="Include country code, e.g. +216 12 345 678")
    photo = models.ImageField(upload_to="contacts/photos/", blank=True, null=True)
    joined_on = models.DateField(null=True, blank=True)
    is_teamleader = models.BooleanField(default=False)

    seller_of_month_count = models.PositiveIntegerField(default=0)
    icebar_of_month_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
