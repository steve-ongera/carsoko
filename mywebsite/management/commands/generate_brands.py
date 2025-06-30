from django.core.management.base import BaseCommand
from mywebsite.models import Brand
from django.conf import settings
import os
from PIL import Image, ImageDraw, ImageFont

class Command(BaseCommand):
    help = 'Generate popular car brands with placeholder logos'

    def handle(self, *args, **kwargs):
        brands = [
            ('Toyota', 'Japan'),
            ('Ford', 'USA'),
            ('BMW', 'Germany'),
            ('Mercedes-Benz', 'Germany'),
            ('Audi', 'Germany'),
            ('Honda', 'Japan'),
            ('Chevrolet', 'USA'),
            ('Nissan', 'Japan'),
            ('Hyundai', 'South Korea'),
            ('Volkswagen', 'Germany'),
            ('Kia', 'South Korea'),
            ('Peugeot', 'France'),
            ('Lexus', 'Japan'),
            ('Mazda', 'Japan'),
            ('Subaru', 'Japan'),
            ('Volvo', 'Sweden'),
            ('Ferrari', 'Italy'),
            ('Lamborghini', 'Italy'),
            ('Porsche', 'Germany'),
            ('Jaguar', 'UK'),
        ]

        logos_dir = os.path.join(settings.MEDIA_ROOT, 'brand_logos')
        os.makedirs(logos_dir, exist_ok=True)

        for name, country in brands:
            brand, created = Brand.objects.get_or_create(
                name=name,
                defaults={'country_of_origin': country}
            )

            if created:
                # Create placeholder image
                logo_path = os.path.join(logos_dir, f"{name.lower().replace(' ', '_')}.png")
                self.generate_logo(name, logo_path)
                brand.logo.name = f"brand_logos/{os.path.basename(logo_path)}"
                brand.save()
                self.stdout.write(self.style.SUCCESS(f"Added brand: {name}"))
            else:
                self.stdout.write(f"Brand already exists: {name}")

    def generate_logo(self, text, path):
        img = Image.new('RGB', (300, 100), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)

        try:
            font_path = os.path.join(settings.BASE_DIR, 'arial.ttf')
            font = ImageFont.truetype(font_path, 24)
        except:
            font = ImageFont.load_default()

        draw.text((10, 35), text, fill=(255, 255, 255), font=font)
        img.save(path)
