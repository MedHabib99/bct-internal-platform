from django.db import models
from django.conf import settings

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=300)
    max_participants = models.IntegerField(null=True, blank=True, help_text="Leave empty for unlimited")
    participants_visible_to = models.CharField(
        max_length=20,
        choices=[
            ('everyone', 'Everyone can see participants'),
            ('teamleaders', 'Only TeamLeaders can see participants'),
        ],
        default='everyone',
        help_text="Who can see the list of participants"
    )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title
    
    def participant_count(self):
        return self.participants.filter(status='yes').count()
    
    def is_full(self):
        if self.max_participants:
            return self.participant_count() >= self.max_participants
        return False


class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_rsvps')
    status = models.CharField(max_length=20, choices=[
        ('yes', 'Yes'),
        ('no', 'No'),
        ('going', 'Going'),
        ('maybe', 'Maybe'),
        ('not_going', 'Not Going'),
    ])
    responded_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['event', 'user'], name='unique_event_user_rsvp')
        ]
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.status})"
