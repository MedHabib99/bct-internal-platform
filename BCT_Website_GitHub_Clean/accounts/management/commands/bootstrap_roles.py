from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Create default roles/groups."

    def handle(self, *args, **kwargs):
        Group.objects.get_or_create(name="TeamLeaders")
        self.stdout.write(self.style.SUCCESS("Roles ensured: TeamLeaders"))
