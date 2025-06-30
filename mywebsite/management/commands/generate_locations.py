from django.core.management.base import BaseCommand
from mywebsite.models import Location

class Command(BaseCommand):
    help = 'Generate major city/town locations in Kenya'

    def handle(self, *args, **kwargs):
        locations = [
            ("Nairobi", "Nairobi"),
            ("Mombasa", "Mombasa"),
            ("Kisumu", "Kisumu"),
            ("Nakuru", "Nakuru"),
            ("Eldoret", "Uasin Gishu"),
            ("Thika", "Kiambu"),
            ("Nyeri", "Nyeri"),
            ("Meru", "Meru"),
            ("Kakamega", "Kakamega"),
            ("Kitale", "Trans Nzoia"),
            ("Garissa", "Garissa"),
            ("Machakos", "Machakos"),
            ("Embu", "Embu"),
            ("Kericho", "Kericho"),
            ("Naivasha", "Nakuru"),
            ("Malindi", "Kilifi"),
            ("Isiolo", "Isiolo"),
        ]

        total_created = 0

        for name, county in locations:
            obj, created = Location.objects.get_or_create(name=name, county=county)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added location: {name}, {county}"))
                total_created += 1
            else:
                self.stdout.write(f"Location already exists: {name}, {county}")

        self.stdout.write(self.style.SUCCESS(f"Total new locations added: {total_created}"))
