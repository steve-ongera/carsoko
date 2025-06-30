import random
import string
from django.utils.text import slugify
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from mywebsite.models import (
    BusinessConfig, Testimonial, BlogPost, FAQ,
    Car  # Ensure Car model has data
)

class Command(BaseCommand):
    help = 'Generate business config, testimonials, blog posts, and FAQs'

    def handle(self, *args, **kwargs):
        self.generate_business_config()
        self.generate_testimonials()
        self.generate_blog_posts()
        self.generate_faqs()
        self.stdout.write(self.style.SUCCESS("✔ All demo business content generated."))

    def generate_business_config(self):
        if BusinessConfig.objects.exists():
            self.stdout.write("BusinessConfig already exists.")
            return
        
        BusinessConfig.objects.create(
            business_name="AutoMart Kenya",
            business_phone="+254712345678",
            whatsapp_number="+254712345678",
            business_email="info@automart.co.ke",
            business_address="Ngong Road, Nairobi, Kenya",
            website_title="AutoMart Kenya - Quality Cars for Sale & Hire",
            website_description="Find new and used cars, car rentals, blogs, and trusted testimonials at AutoMart Kenya.",
            website_keywords="cars for sale, kenya cars, toyota, rentals, automart kenya",
            facebook_url="https://facebook.com/automartkenya",
            instagram_url="https://instagram.com/automartkenya",
            twitter_url="https://twitter.com/automartke"
        )
        self.stdout.write(self.style.SUCCESS("✔ Created BusinessConfig"))

    def generate_testimonials(self):
        cars = list(Car.objects.all())
        if not cars:
            self.stdout.write(self.style.WARNING("⚠ Skipping Testimonial: No cars found."))
            return

        names = ["John Mwangi", "Faith Wanjiru", "Alex Mutua", "Diana Otieno", "Brian Kipkoech"]
        locations = ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret"]
        messages = [
            "Excellent customer service and smooth transaction!",
            "I love my new car. It’s in perfect condition!",
            "Fast and reliable. I highly recommend AutoMart.",
            "The team helped me through every step.",
            "Got a good deal and quick delivery!"
        ]

        for i in range(5):
            Testimonial.objects.create(
                customer_name=names[i],
                customer_location=locations[i],
                message=messages[i],
                rating=random.randint(4, 5),
                car_purchased=random.choice(cars),
                is_featured=True,
                is_approved=True
            )
        self.stdout.write(self.style.SUCCESS("✔ Created 5 Testimonials"))

    def generate_blog_posts(self):
        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.WARNING("⚠ Skipping BlogPost: No users found."))
            return
        
        titles = [
            "How to Choose the Right Car in Kenya",
            "Why Foreign Used Cars are Popular",
            "Top 10 Fuel-Efficient Cars in Kenya"
        ]
        contents = [
            "When choosing a car in Kenya, consider budget, fuel efficiency, maintenance, and resale value.",
            "Foreign used cars offer better quality, lower mileage, and more features compared to locally used ones.",
            "Check out these top fuel-saving vehicles that are perfect for Kenyan roads."
        ]

        for i in range(3):
            title = titles[i]
            BlogPost.objects.create(
                title=title,
                slug=slugify(title + '-' + ''.join(random.choices(string.ascii_lowercase, k=5))),
                content=contents[i],
                excerpt=contents[i][:150] + "...",
                meta_title=title,
                meta_description=contents[i][:150],
                is_published=True,
                published_at=timezone.now(),
                author=random.choice(users)
            )
        self.stdout.write(self.style.SUCCESS("✔ Created 3 Blog Posts"))

    def generate_faqs(self):
        faqs = [
            ("How can I buy a car?", "Visit our listings, contact us, and schedule a viewing.", "buying"),
            ("What documents are required for purchase?", "ID, KRA PIN, and proof of payment.", "buying"),
            ("Can I list my car for sale?", "Yes, contact our sales team to get started.", "selling"),
            ("Do you offer rental cars?", "Yes, check our car rental section for available vehicles.", "rental"),
            ("Do you provide car financing?", "We work with partners to offer financing options.", "financing"),
            ("Where are you located?", "We are based on Ngong Road, Nairobi.", "general"),
        ]

        for i, (question, answer, category) in enumerate(faqs):
            FAQ.objects.create(
                question=question,
                answer=answer,
                category=category,
                order=i
            )
        self.stdout.write(self.style.SUCCESS(f"✔ Created {len(faqs)} FAQs"))
