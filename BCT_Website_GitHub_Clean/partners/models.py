from django.db import models

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

