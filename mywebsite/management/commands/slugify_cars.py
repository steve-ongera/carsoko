from django.core.management.base import BaseCommand
from django.utils.text import slugify
from mywebsite.models import Car

class Command(BaseCommand):
    help = "Generate unique slugs for all cars that don't have one"

    def handle(self, *args, **kwargs):
        updated = 0

        for car in Car.objects.filter(slug__isnull=True):
            base_slug = slugify(f"{car.year}-{car.brand.name}-{car.car_model.name}")
            slug = base_slug
            counter = 1
            while Car.objects.filter(slug=slug).exclude(pk=car.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            car.slug = slug
            car.save(update_fields=['slug'])
            updated += 1
            self.stdout.write(self.style.SUCCESS(f"Updated slug: {car} → {slug}"))

        self.stdout.write(self.style.SUCCESS(f"Total cars updated with slugs: {updated}"))
