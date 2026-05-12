from django.core.management.base import BaseCommand
from django.utils.text import slugify
from worksafety.models import (
    WorkSafetyCategory,
    WorkSafetyEmergencyInfo
)


class Command(BaseCommand):
    help = 'Set up initial Work Safety categories and emergency information'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up Work Safety module...'))

        categories_data = [
            ('General Safety Guidelines', 1),
            ('Emergency Procedures', 2),
            ('Equipment Safety', 3),
            ('First Aid', 4),
            ('Fire Safety', 5),
            ('Workplace Hazards', 6),
        ]

        created_count = 0
        for name, order in categories_data:
            category, created = WorkSafetyCategory.objects.get_or_create(
                slug=slugify(name),
                defaults={
                    'name': name,
                    'order': order
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f'  Created category: {name}')
            else:
                self.stdout.write(f'  Category already exists: {name}')

        emergency_info = WorkSafetyEmergencyInfo.get_instance()
        if not emergency_info.company_contact_name:
            emergency_info.emergency_number = '112'
            emergency_info.police_number = '110'
            emergency_info.company_contact_name = 'Safety Officer'
            emergency_info.company_contact_phone = '+49 123 456 789'
            emergency_info.quick_steps = '''1. Stay calm and assess the situation
2. Call emergency services (112) if needed
3. Secure the area and prevent further harm
4. Provide first aid if trained
5. Notify your team leader or safety officer
6. Document the incident'''
            emergency_info.save()
            self.stdout.write(self.style.SUCCESS('  Created emergency information'))
        else:
            self.stdout.write('  Emergency information already exists')

        self.stdout.write(self.style.SUCCESS(f'\nSetup complete! Created {created_count} new categories.'))
        self.stdout.write(self.style.SUCCESS('You can now upload safety documents through the admin panel or web interface.'))
