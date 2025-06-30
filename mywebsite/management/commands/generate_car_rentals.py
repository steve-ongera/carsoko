import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from mywebsite.models import Car, CarRental

class Command(BaseCommand):
    help = 'Randomly select 20 cars and make them available for rental'

    def handle(self, *args, **kwargs):
        cars = list(Car.objects.exclude(rental_info__isnull=False))  # Only cars not already rented
        if len(cars) < 20:
            self.stdout.write(self.style.ERROR("Not enough unrented cars in the database (need at least 20)."))
            return

        selected_cars = random.sample(cars, 20)
        created_count = 0

        for car in selected_cars:
            daily_rate = Decimal(random.randint(3000, 10000))
            weekly_rate = daily_rate * 7 * Decimal('0.9')  # 10% discount for weekly
            monthly_rate = daily_rate * 30 * Decimal('0.8')  # 20% discount for monthly
            deposit = daily_rate * Decimal('2')

            rental = CarRental.objects.create(
                car=car,
                daily_rate=daily_rate,
                weekly_rate=weekly_rate,
                monthly_rate=monthly_rate,
                minimum_age=random.choice([21, 23, 25]),
                requires_license=True,
                requires_deposit=True,
                deposit_amount=deposit,
                max_rental_days=random.randint(15, 60),
                mileage_limit_per_day=random.choice([100, 150, 200]),
                extra_mileage_charge=Decimal(random.choice([10, 15, 20])),
                rental_status=random.choice([s[0] for s in CarRental.RENTAL_STATUS_CHOICES]),
                terms_and_conditions="Driver must have a valid license. Deposit refundable upon return.",
            )
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f"Created rental: {rental}"))

        self.stdout.write(self.style.SUCCESS(f"Total car rentals created: {created_count}"))
