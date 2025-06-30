import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from mywebsite.models import Car, CarModel, Brand, Location

class Command(BaseCommand):
    help = 'Generate 4-8 car listings for each brand'

    def handle(self, *args, **kwargs):
        if not Location.objects.exists():
            self.stdout.write(self.style.ERROR("Please run generate_locations first. No locations found."))
            return
        
        total_created = 0

        for brand in Brand.objects.all():
            car_models = CarModel.objects.filter(brand=brand)
            if not car_models.exists():
                self.stdout.write(f"Skipping brand '{brand.name}' – no car models.")
                continue

            num_cars = random.randint(4, 8)
            for _ in range(num_cars):
                model = random.choice(car_models)
                year = random.randint(2005, 2023)
                condition = random.choice([c[0] for c in Car.CONDITION_CHOICES])
                engine_size = round(random.uniform(1.0, 5.0), 1)
                fuel_type = random.choice([f[0] for f in Car.FUEL_TYPE_CHOICES])
                transmission = random.choice([t[0] for t in Car.TRANSMISSION_CHOICES])
                drive_type = random.choice([d[0] for d in Car.DRIVE_TYPE_CHOICES])
                mileage = random.randint(10000, 150000)
                color = random.choice(["White", "Black", "Silver", "Blue", "Red", "Grey"])
                doors = random.randint(2, 5)
                seats = random.randint(4, 7)
                price = Decimal(random.randint(800000, 8000000))
                location = random.choice(Location.objects.all())
                status = random.choice([s[0] for s in Car.STATUS_CHOICES])

                car = Car.objects.create(
                    brand=brand,
                    car_model=model,
                    year=year,
                    condition=condition,
                    engine_size=Decimal(str(engine_size)),
                    fuel_type=fuel_type,
                    transmission=transmission,
                    drive_type=drive_type,
                    mileage=mileage,
                    color=color,
                    doors=doors,
                    seats=seats,
                    price=price,
                    negotiable=random.choice([True, False]),
                    status=status,
                    location=location,
                    description=f"A well-maintained {year} {brand.name} {model.name}.",
                    features="Power Steering,Airbags,ABS,Alloy Wheels,Reverse Camera",
                    country_of_import="Japan" if condition == 'used_foreign' else "",
                    import_duty_paid=condition == 'used_foreign' and random.choice([True, False]),
                    is_featured=random.choice([True, False])
                )
                total_created += 1
                self.stdout.write(self.style.SUCCESS(f"Added: {car}"))

        self.stdout.write(self.style.SUCCESS(f"Total cars created: {total_created}"))
