from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class SafetyInfo(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('first_aid', 'First Aid'),
        ('emergency', 'Emergency Contacts'),
        ('procedures', 'Safety Procedures'),
        ('equipment', 'Safety Equipment'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'title']

    def __str__(self):
        return self.title


class WorkSafetyCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers first)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Work Safety Category'
        verbose_name_plural = 'Work Safety Categories'

    def __str__(self):
        return self.name


class WorkSafetyDocument(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]
    VISIBLE_TO_CHOICES = [
        ('everyone', 'Everyone'),
        ('teamleaders', 'Team Leaders Only'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, help_text="Optional document description")
    category = models.ForeignKey(
        WorkSafetyCategory,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    file = models.FileField(upload_to='worksafety/', help_text="Upload PDF, Word, or other document")
    version = models.CharField(max_length=20, default='1.0', help_text="e.g. 1.0, 1.1, 2.0")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    visible_to = models.CharField(
        max_length=20,
        choices=VISIBLE_TO_CHOICES,
        default='everyone',
        help_text="Control who can view this document"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='worksafety_docs'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Work Safety Document'
        verbose_name_plural = 'Work Safety Documents'

    def __str__(self):
        return f"{self.title} (v{self.version})"

    @property
    def is_active(self):
        return self.status == 'active'

    @property
    def is_new(self):
        return timezone.now() - self.updated_at < timedelta(days=14)

    def requires_acknowledgement_for(self, user):
        if not self.is_active:
            return False
        
        latest_ack = self.acks.filter(user=user).order_by('-acknowledged_at').first()
        if not latest_ack:
            return True
        
        return latest_ack.version != self.version

    def get_acknowledgement_count(self):
        return self.acks.filter(version=self.version).count()

    def get_user_acknowledgement(self, user):
        return self.acks.filter(user=user).order_by('-acknowledged_at').first()


class WorkSafetyAcknowledgement(models.Model):
    document = models.ForeignKey(
        WorkSafetyDocument,
        on_delete=models.CASCADE,
        related_name='acks'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='worksafety_acks'
    )
    version = models.CharField(max_length=20, help_text="Document version at time of acknowledgement")
    acknowledged_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-acknowledged_at']
        verbose_name = 'Work Safety Acknowledgement'
        verbose_name_plural = 'Work Safety Acknowledgements'
        constraints = [
            models.UniqueConstraint(
                fields=['document', 'user', 'version'],
                name='unique_document_user_version'
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.document.title} v{self.version}"


class WorkSafetyEmergencyInfo(models.Model):
    emergency_number = models.CharField(max_length=50, default='112', help_text="Emergency services number")
    police_number = models.CharField(max_length=50, default='110', help_text="Police number")
    company_contact_name = models.CharField(max_length=100, blank=True, help_text="Company emergency contact name")
    company_contact_phone = models.CharField(max_length=50, blank=True, help_text="Company emergency contact phone")
    quick_steps = models.TextField(
        help_text="Quick emergency action steps (3-6 bullet points, one per line)"
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='emergency_info_updates'
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Emergency Information'
        verbose_name_plural = 'Emergency Information'

    def __str__(self):
        return "Emergency Information"

    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class WorkSafetyIncidentReport(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('reviewed', 'Reviewed'),
        ('closed', 'Closed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Describe what happened")
    location = models.CharField(max_length=200, blank=True, help_text="Where did this occur?")
    occurred_at = models.DateTimeField(help_text="When did this occur?")
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='incident_reports'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')

    class Meta:
        ordering = ['-occurred_at']
        verbose_name = 'Incident Report'
        verbose_name_plural = 'Incident Reports'

    def __str__(self):
        return f"{self.title} - {self.occurred_at.strftime('%Y-%m-%d')}"
