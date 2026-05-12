from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        TEAMLEADER = "TEAMLEADER", "Teamleader"
        SELLER = "SELLER", "Seller"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.SELLER,
    )

    def save(self, *args, **kwargs):
        if self.role == self.Role.TEAMLEADER:
            self.is_staff = True
            self.is_superuser = True
        elif self.role == self.Role.SELLER:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)

    def is_teamleader(self):
        return self.role == self.Role.TEAMLEADER

import secrets, string, datetime as dt
from django.utils import timezone
from django.conf import settings
from django.db import models

def _generate_otp(length=6):
    return ''.join(secrets.choice(string.digits) for _ in range(length))

class EmailOTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="email_otps")
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    consumed_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)
    sent_count = models.PositiveSmallIntegerField(default=1)
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)

    class Meta:
        indexes = [models.Index(fields=["user", "created_at"])]

    @classmethod
    def create_for_user(cls, user, ip=None, ua=""):
        cls.objects.filter(user=user, consumed_at__isnull=True).delete()
        now = timezone.now()
        return cls.objects.create(
            user=user,
            code=_generate_otp(6),
            expires_at=now + dt.timedelta(minutes=5),
            ip=ip,
            user_agent=(ua or "")[:255],
        )

    def is_expired(self):
        return timezone.now() > self.expires_at

    def consume(self):
        self.consumed_at = timezone.now()
        self.save(update_fields=["consumed_at"])

