from django.core.management.base import BaseCommand
from properties.models import Property
from decimal import Decimal


class Command(BaseCommand):
    help = 'Create sample properties for testing'

    def handle(self, *args, **options):
        sample_properties = [
            {
                'title': 'Modern Downtown Apartment',
                'description': 'Beautiful 2-bedroom apartment in the heart of downtown with amazing city views.',
                'price': Decimal('2500.00'),
                'location': 'Downtown'
            },
            {
                'title': 'Cozy Suburban House',
                'description': 'Family-friendly 3-bedroom house with a large backyard and garage.',
                'price': Decimal('4500.00'),
                'location': 'Suburbs'
            },
            {
                'title': 'Luxury Penthouse',
                'description': 'Stunning penthouse with panoramic views, high-end finishes, and rooftop terrace.',
                'price': Decimal('8500.00'),
                'location': 'Uptown'
            },
            {
                'title': 'Student Studio',
                'description': 'Affordable studio apartment perfect for students, close to university campus.',
                'price': Decimal('1200.00'),
                'location': 'University District'
            },
            {
                'title': 'Waterfront Condo',
                'description': 'Spacious 2-bedroom condo with waterfront views and private balcony.',
                'price': Decimal('3800.00'),
                'location': 'Waterfront'
            }
        ]

        created_count = 0
        for prop_data in sample_properties:
            property_obj, created = Property.objects.get_or_create(
                title=prop_data['title'],
                defaults=prop_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created property: {property_obj.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Property already exists: {property_obj.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new properties')
        )
