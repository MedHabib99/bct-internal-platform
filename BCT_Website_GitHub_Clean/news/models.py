from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from datetime import timedelta


class NewsCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "News Category"
        verbose_name_plural = "News Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class NewsArticle(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(
        NewsCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='articles'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        help_text="Draft articles are only visible to teamleaders"
    )
    publish_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date when the article was/will be published. Auto-set when status changes to Published."
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_news'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='authored_news'
    )
    is_important = models.BooleanField(default=False, help_text="Pin to top")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_important', '-publish_date', '-created_at']
        verbose_name = "News Article"
        verbose_name_plural = "News Articles"

    def __str__(self):
        return self.title

    @property
    def is_new(self):
        if self.status != 'published' or not self.publish_date:
            return False
        
        threshold = timezone.now() - timedelta(days=3)
        return self.publish_date >= threshold

    def get_author(self):
        return self.created_by or self.author
