import random
from django.core.management.base import BaseCommand
from mywebsite.models import Brand, CarModel

class Command(BaseCommand):
    help = 'Generate common car models for each existing brand'

    brand_models = {
        "Toyota": ["Corolla", "Camry", "RAV4", "Land Cruiser", "Hilux"],
        "Ford": ["F-150", "Focus", "Mustang", "Explorer", "Escape"],
        "BMW": ["3 Series", "5 Series", "X3", "X5", "i8"],
        "Mercedes-Benz": ["C-Class", "E-Class", "S-Class", "GLE", "GLA"],
        "Audi": ["A3", "A4", "A6", "Q5", "Q7"],
        "Honda": ["Civic", "Accord", "CR-V", "Fit", "Pilot"],
        "Chevrolet": ["Silverado", "Malibu", "Equinox", "Camaro", "Impala"],
        "Nissan": ["Altima", "Sentra", "Rogue", "Frontier", "Leaf"],
        "Hyundai": ["Elantra", "Tucson", "Santa Fe", "Sonata", "Kona"],
        "Volkswagen": ["Golf", "Passat", "Tiguan", "Jetta", "Polo"],
        "Kia": ["Rio", "Sportage", "Sorento", "Soul", "Optima"],
        "Peugeot": ["208", "308", "508", "2008", "3008"],
        "Lexus": ["RX", "NX", "ES", "IS", "GX"],
        "Mazda": ["Mazda3", "Mazda6", "CX-5", "CX-9", "MX-5"],
        "Subaru": ["Outback", "Forester", "Impreza", "WRX", "Ascent"],
        "Volvo": ["S60", "XC40", "XC60", "XC90", "V60"],
        "Ferrari": ["488 GTB", "Roma", "Portofino", "SF90", "F8"],
        "Lamborghini": ["Aventador", "Huracan", "Urus", "Gallardo", "Murcielago"],
        "Porsche": ["911", "Cayenne", "Macan", "Panamera", "Taycan"],
        "Jaguar": ["XE", "XF", "F-Pace", "E-Pace", "F-Type"],
    }

    body_types = [
        'sedan', 'suv', 'hatchback', 'coupe',
        'convertible', 'wagon', 'pickup', 'van', 'crossover'
    ]

    def handle(self, *args, **kwargs):
        total_created = 0

        for brand in Brand.objects.all():
            models = self.brand_models.get(brand.name, [])
            for model_name in models:
                obj, created = CarModel.objects.get_or_create(
                    brand=brand,
                    name=model_name,
                    defaults={
                        'body_type': random.choice(self.body_types),
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f"Created model: {obj}"))
                    total_created += 1
                else:
                    self.stdout.write(f"Model already exists: {obj}")
        
        self.stdout.write(self.style.SUCCESS(f"Total new car models added: {total_created}"))
