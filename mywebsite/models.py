from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from PIL import Image
import os
from django.utils.text import slugify

# Car Brand Model
class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField( blank=True, null=True)  # NEW FIELD
    logo = models.ImageField(upload_to='brand_logos/', blank=True, null=True)
    country_of_origin = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Brand.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']

# Car Model
class CarModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='car_models')
    name = models.CharField(max_length=100)
    body_type = models.CharField(max_length=50, choices=[
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('hatchback', 'Hatchback'),
        ('coupe', 'Coupe'),
        ('convertible', 'Convertible'),
        ('wagon', 'Station Wagon'),
        ('pickup', 'Pickup Truck'),
        ('van', 'Van'),
        ('crossover', 'Crossover'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.brand.name} {self.name}"
    
    class Meta:
        ordering = ['brand__name', 'name']
        unique_together = ['brand', 'name']

# Location Model
class Location(models.Model):
    name = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name}, {self.county}"
    
    class Meta:
        ordering = ['county', 'name']

# Main Car Model
class Car(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Brand New'),
        ('used_local', 'Used (Local)'),
        ('used_foreign', 'Used (Foreign Import)'),
    ]
    
    FUEL_TYPE_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('hybrid', 'Hybrid'),
        ('electric', 'Electric'),
        ('lpg', 'LPG'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
        ('cvt', 'CVT'),
    ]
    
    DRIVE_TYPE_CHOICES = [
        ('fwd', 'Front Wheel Drive'),
        ('rwd', 'Rear Wheel Drive'),
        ('awd', 'All Wheel Drive'),
        ('4wd', '4 Wheel Drive'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('reserved', 'Reserved'),
        ('under_maintenance', 'Under Maintenance'),
    ]
    
    # Basic Information
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2030)])
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    
    # Technical Specifications
    engine_size = models.DecimalField(max_digits=3, decimal_places=1, help_text="Engine size in liters")
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    drive_type = models.CharField(max_length=10, choices=DRIVE_TYPE_CHOICES)
    mileage = models.IntegerField(help_text="Mileage in kilometers")
    
    # Physical Specifications
    color = models.CharField(max_length=50)
    doors = models.IntegerField(validators=[MinValueValidator(2), MaxValueValidator(5)])
    seats = models.IntegerField(validators=[MinValueValidator(2), MaxValueValidator(9)])
    
    # Pricing and Availability
    price = models.DecimalField(max_digits=10, decimal_places=2)
    negotiable = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    
    # Location and Contact
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    
    # Additional Information
    description = models.TextField(blank=True, null=True)
    features = models.TextField(blank=True, null=True, help_text="List of features separated by commas")
    
    # Import Information (for foreign used cars)
    country_of_import = models.CharField(max_length=100, blank=True, null=True)
    import_duty_paid = models.BooleanField(default=False)

    slug = models.SlugField( blank=True, null=True)  
    
    # Metadata
    is_featured = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.year} {self.brand.name} {self.car_model.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.year}-{self.brand.name}-{self.car_model.name}")
            slug = base_slug
            counter = 1
            while Car.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])

    class Meta:
        ordering = ['-created_at']

# Car Images Model
class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='car_images/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Ensure only one primary image per car
        if self.is_primary:
            CarImage.objects.filter(car=self.car, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)
        
        # Resize image to optimize storage
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 1200:
                output_size = (1200, 800)
                img.thumbnail(output_size)
                img.save(self.image.path)
    
    def __str__(self):
        return f"Image for {self.car}"
    
    class Meta:
        ordering = ['order', 'uploaded_at']

# Car Rental Model
class CarRental(models.Model):
    RENTAL_STATUS_CHOICES = [
        ('available', 'Available'),
        ('rented', 'Currently Rented'),
        ('maintenance', 'Under Maintenance'),
        ('unavailable', 'Unavailable'),
    ]
    
    car = models.OneToOneField(Car, on_delete=models.CASCADE, related_name='rental_info')
    daily_rate = models.DecimalField(max_digits=8, decimal_places=2)
    weekly_rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    monthly_rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    
    # Rental Requirements
    minimum_age = models.IntegerField(default=21)
    requires_license = models.BooleanField(default=True)
    requires_deposit = models.BooleanField(default=True)
    deposit_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    
    # Rental Terms
    max_rental_days = models.IntegerField(default=30)
    mileage_limit_per_day = models.IntegerField(blank=True, null=True, help_text="Daily mileage limit in KM")
    extra_mileage_charge = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    rental_status = models.CharField(max_length=20, choices=RENTAL_STATUS_CHOICES, default='available')
    terms_and_conditions = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Rental: {self.car}"

# Customer Inquiry Model
class CustomerInquiry(models.Model):
    INQUIRY_TYPE_CHOICES = [
        ('purchase', 'Purchase Inquiry'),
        ('rental', 'Rental Inquiry'),
        ('general', 'General Inquiry'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]
    
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='inquiries', blank=True, null=True)
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPE_CHOICES)
    
    # Customer Information
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField(blank=True, null=True)
    
    # Inquiry Details
    message = models.TextField()
    preferred_contact_method = models.CharField(max_length=20, choices=[
        ('phone', 'Phone Call'),
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
    ], default='whatsapp')
    
    # Status and Follow-up
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    notes = models.TextField(blank=True, null=True, help_text="Internal notes")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Inquiry from {self.customer_name} - {self.inquiry_type}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Customer Inquiries"

# Business Configuration Model
class BusinessConfig(models.Model):
    business_name = models.CharField(max_length=200)
    business_phone = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20)
    business_email = models.EmailField()
    business_address = models.TextField()
    
    # WhatsApp Integration
    whatsapp_message_template = models.TextField(
        default="Hello! I'm interested in your {car_year} {car_brand} {car_model}. Price: KES {car_price}. Is it still available?",
        help_text="Use placeholders: {car_year}, {car_brand}, {car_model}, {car_price}"
    )
    
    # Business Hours
    opening_hours = models.CharField(max_length=100, default="Mon-Sat: 8:00 AM - 6:00 PM")
    
    # SEO and Marketing
    website_title = models.CharField(max_length=200)
    website_description = models.TextField()
    website_keywords = models.TextField(blank=True, null=True)
    
    # Social Media
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.business_name
    
    class Meta:
        verbose_name = "Business Configuration"
        verbose_name_plural = "Business Configuration"

# Testimonial Model
class Testimonial(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_location = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    car_purchased = models.ForeignKey(Car, on_delete=models.SET_NULL, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Testimonial from {self.customer_name}"
    
    class Meta:
        ordering = ['-created_at']

# Blog/News Model
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True, null=True)
    featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.TextField(max_length=300, blank=True, null=True)
    
    # Publication
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Engagement
    views_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-published_at']

# FAQ Model
class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('buying', 'Buying Cars'),
        ('selling', 'Selling Cars'),
        ('rental', 'Car Rental'),
        ('financing', 'Financing'),
        ('general', 'General'),
    ]
    
    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question
    
    class Meta:
        ordering = ['category', 'order']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

# Car Comparison Model (for users to compare cars)
class CarComparison(models.Model):
    cars = models.ManyToManyField(Car, related_name='comparisons')
    session_key = models.CharField(max_length=100)  # For anonymous users
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comparison - {self.created_at}"
    
    class Meta:
        ordering = ['-created_at']

# Newsletter Subscription Model
class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    
    class Meta:
        ordering = ['-subscribed_at']

# Contact Message Model
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
    
    class Meta:
        ordering = ['-created_at']