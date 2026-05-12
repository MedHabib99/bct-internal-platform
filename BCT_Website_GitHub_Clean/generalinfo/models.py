from django.db import models

class InfoPage(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('vouchers', 'Vouchers'),
        ('company', 'Company Info'),
        ('tours', 'Tour Information'),
        ('policies', 'Policies'),
        ('benefits', 'Employee Benefits'),
    ])
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'order', 'title']

    def __str__(self):
        return self.title

