# Car Dealership Management System

**Author:** Steve Ongera  
**Framework:** Django  
**Version:** 1.0.0  

A comprehensive Django-based car dealership management system designed for the Kenyan automotive market. This system handles car sales, rentals, customer inquiries, and business management with a focus on local market requirements.

## 🚗 Features

### Core Functionality
- **Car Inventory Management** - Complete car catalog with detailed specifications
- **Brand & Model Management** - Organized brand hierarchy with model relationships
- **Location-Based Listings** - County and town-based car locations
- **Car Rental System** - Integrated rental management with terms and pricing
- **Customer Inquiry System** - Lead management and customer communication
- **Image Management** - Multiple car images with automatic optimization
- **Business Configuration** - Centralized business settings and branding

### Advanced Features
- **WhatsApp Integration** - Direct WhatsApp messaging for inquiries
- **Car Comparison** - Side-by-side car comparison functionality
- **Testimonials & Reviews** - Customer feedback and rating system
- **Blog/News System** - Content management for automotive news
- **Newsletter Management** - Email subscription system
- **FAQ System** - Categorized frequently asked questions
- **SEO Optimization** - Built-in SEO features for better visibility

## 📋 Models Overview

### Primary Models

#### `Brand`
Manages car manufacturers and their information.
```python
- name: CharField (unique brand name)
- logo: ImageField (brand logo)
- country_of_origin: CharField
- created_at: DateTimeField
```

#### `CarModel`
Links specific car models to their respective brands.
```python
- brand: ForeignKey to Brand
- name: CharField (model name)
- body_type: CharField (sedan, suv, hatchback, etc.)
- created_at: DateTimeField
```

#### `Car`
The main inventory model containing all car details.
```python
# Basic Information
- brand: ForeignKey to Brand
- car_model: ForeignKey to CarModel
- year: IntegerField (1900-2030)
- condition: CharField (new, used_local, used_foreign)

# Technical Specifications
- engine_size: DecimalField (in liters)
- fuel_type: CharField (petrol, diesel, hybrid, electric, lpg)
- transmission: CharField (manual, automatic, cvt)
- drive_type: CharField (fwd, rwd, awd, 4wd)
- mileage: IntegerField (in kilometers)

# Physical Specifications
- color: CharField
- doors: IntegerField (2-5)
- seats: IntegerField (2-9)

# Pricing and Status
- price: DecimalField
- negotiable: BooleanField
- status: CharField (available, sold, reserved, under_maintenance)

# Additional Features
- description: TextField
- features: TextField (comma-separated)
- is_featured: BooleanField
- views_count: IntegerField
```

#### `Location`
Manages geographical locations for car listings.
```python
- name: CharField (town/city name)
- county: CharField (Kenyan county)
- is_active: BooleanField
```

### Supporting Models

#### `CarImage`
Handles multiple images per car with automatic optimization.
```python
- car: ForeignKey to Car
- image: ImageField (auto-resized to 1200x800)
- caption: CharField
- is_primary: BooleanField (one per car)
- order: IntegerField (display order)
```

#### `CarRental`
Manages rental-specific information for cars.
```python
- car: OneToOneField to Car
- daily_rate: DecimalField
- weekly_rate: DecimalField (optional)
- monthly_rate: DecimalField (optional)
- minimum_age: IntegerField (default: 21)
- requires_license: BooleanField
- deposit_amount: DecimalField
- mileage_limit_per_day: IntegerField
- rental_status: CharField
```

#### `CustomerInquiry`
Tracks customer interactions and leads.
```python
- car: ForeignKey to Car (optional)
- inquiry_type: CharField (purchase, rental, general)
- customer_name: CharField
- customer_phone: CharField
- customer_email: EmailField
- message: TextField
- preferred_contact_method: CharField (phone, whatsapp, email)
- status: CharField (new, contacted, in_progress, closed)
```

### Business Management Models

#### `BusinessConfig`
Centralized business configuration and settings.
```python
- business_name: CharField
- business_phone: CharField
- whatsapp_number: CharField
- business_email: EmailField
- business_address: TextField
- whatsapp_message_template: TextField
- opening_hours: CharField
- website_title: CharField
- website_description: TextField
- social_media_urls: URLField (Facebook, Instagram, Twitter)
```

#### `Testimonial`
Customer reviews and testimonials.
```python
- customer_name: CharField
- customer_location: CharField
- message: TextField
- rating: IntegerField (1-5)
- car_purchased: ForeignKey to Car (optional)
- is_featured: BooleanField
- is_approved: BooleanField
```

### Content Management Models

#### `BlogPost`
News and blog content management.
```python
- title: CharField
- slug: SlugField (unique)
- content: TextField
- excerpt: TextField
- featured_image: ImageField
- meta_title: CharField (SEO)
- meta_description: TextField (SEO)
- is_published: BooleanField
- author: ForeignKey to User
- views_count: IntegerField
```

#### `FAQ`
Frequently asked questions by category.
```python
- question: CharField
- answer: TextField
- category: CharField (buying, selling, rental, financing, general)
- order: IntegerField
- is_active: BooleanField
```

### Utility Models

#### `CarComparison`
Enables users to compare multiple cars.
```python
- cars: ManyToManyField to Car
- session_key: CharField (for anonymous users)
- user: ForeignKey to User (optional)
```

#### `NewsletterSubscription`
Email newsletter management.
```python
- email: EmailField (unique)
- is_active: BooleanField
- subscribed_at: DateTimeField
```

#### `ContactMessage`
General contact form submissions.
```python
- name: CharField
- email: EmailField
- phone: CharField
- subject: CharField
- message: TextField
- is_read: BooleanField
```

## 🛠 Installation & Setup

### Prerequisites
```bash
Python 3.8+
Django 4.0+
Pillow (for image handling)
```

### Installation Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd car-dealership
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install django pillow
```

4. **Apply migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser**
```bash
python manage.py createsuperuser
```

6. **Run the development server**
```bash
python manage.py runserver
```

## 📱 WhatsApp Integration

The system includes built-in WhatsApp integration for customer inquiries:

- Customizable message templates in `BusinessConfig`
- Direct WhatsApp links for each car listing
- Template variables: `{car_year}`, `{car_brand}`, `{car_model}`, `{car_price}`

Example template:
```
Hello! I'm interested in your {car_year} {car_brand} {car_model}. 
Price: KES {car_price}. Is it still available?
```

## 🎯 Key Features for Kenyan Market

### Localization
- **County-based locations** - Aligns with Kenyan administrative divisions
- **Import duty tracking** - For foreign used cars
- **KES pricing** - Kenyan Shilling currency support
- **WhatsApp integration** - Primary communication method in Kenya

### Car Conditions
- **Brand New** - Fresh from dealership
- **Used (Local)** - Previously owned in Kenya
- **Used (Foreign Import)** - Imported used vehicles

### Business Features
- **Negotiable pricing** - Common in Kenyan car trade
- **Featured listings** - Promotional car highlights
- **Multiple contact methods** - Phone, WhatsApp, Email
- **Rental integration** - Growing car rental market

## 🔧 Model Methods & Properties

### Car Model Methods
```python
def increment_views(self):
    """Safely increment view counter"""
    
def __str__(self):
    """Returns formatted car name: '2020 Toyota Camry'"""
```

### CarImage Model Methods
```python
def save(self, *args, **kwargs):
    """Auto-resize images and manage primary image logic"""
```

### Business Logic
- **Automatic image optimization** - Resizes to 1200x800 pixels
- **Primary image management** - Only one primary image per car
- **View counting** - Track car listing popularity
- **Status management** - Car availability tracking

## 📊 Admin Interface

All models are designed to work seamlessly with Django Admin:

- **Organized model groupings** - Logical admin sections
- **Search and filter capabilities** - Easy data management
- **Inline editing** - Car images managed within car records
- **Custom ordering** - Sensible default sorting

## 🚀 Usage Examples

### Creating a Car Listing
```python
from myapp.models import Brand, CarModel, Car, Location

# Create or get brand
toyota, created = Brand.objects.get_or_create(
    name="Toyota",
    defaults={'country_of_origin': 'Japan'}
)

# Create or get model
camry, created = CarModel.objects.get_or_create(
    brand=toyota,
    name="Camry",
    defaults={'body_type': 'sedan'}
)

# Create location
nairobi, created = Location.objects.get_or_create(
    name="Nairobi",
    county="Nairobi"
)

# Create car listing
car = Car.objects.create(
    brand=toyota,
    car_model=camry,
    year=2020,
    condition='used_local',
    engine_size=2.5,
    fuel_type='petrol',
    transmission='automatic',
    drive_type='fwd',
    mileage=50000,
    color='Silver',
    doors=4,
    seats=5,
    price=2500000,  # KES 2.5M
    location=nairobi,
    description="Well maintained family car"
)
```

### Adding Car Images
```python
from myapp.models import CarImage

# Add primary image
CarImage.objects.create(
    car=car,
    image='path/to/image.jpg',
    is_primary=True,
    caption='Front view'
)

# Add additional images
CarImage.objects.create(
    car=car,
    image='path/to/interior.jpg',
    order=1,
    caption='Interior view'
)
```

## 🔍 Search & Filtering

The models support various filtering options:

### Common Filters
```python
# Filter by brand
toyota_cars = Car.objects.filter(brand__name='Toyota')

# Filter by price range
affordable_cars = Car.objects.filter(price__lte=1500000)

# Filter by location
nairobi_cars = Car.objects.filter(location__county='Nairobi')

# Filter available cars
available_cars = Car.objects.filter(status='available')

# Filter by fuel type
hybrid_cars = Car.objects.filter(fuel_type='hybrid')
```

### Advanced Filtering
```python
# Cars under 2M, automatic, in Nairobi
filtered_cars = Car.objects.filter(
    price__lt=2000000,
    transmission='automatic',
    location__county='Nairobi',
    status='available'
).select_related('brand', 'car_model', 'location')
```

## 📈 Performance Considerations

### Database Optimization
- **Foreign key relationships** - Proper indexing for fast queries
- **Select related** - Minimize database hits
- **Image optimization** - Automatic resizing to reduce storage
- **Ordering** - Sensible default ordering for all models

### Recommended Indexes
```python
# Custom indexes for heavy queries
class Meta:
    indexes = [
        models.Index(fields=['brand', 'price']),
        models.Index(fields=['location', 'status']),
        models.Index(fields=['fuel_type', 'transmission']),
    ]
```

## 🔒 Security Features

- **Input validation** - Min/Max validators on critical fields
- **Image processing** - Safe image handling with Pillow
- **XSS protection** - TextField content requires proper sanitization
- **File upload security** - Restricted upload paths and file types

## 📝 Contributing

This project follows Django best practices:

1. **Model Design** - Clear relationships and proper field types
2. **Naming Conventions** - Descriptive model and field names
3. **Documentation** - Comprehensive docstrings and help text
4. **Validation** - Proper field validation and constraints

## 📞 Support

**Developer:** Steve Ongera  
**Email:** [your-email@domain.com]  
**GitHub:** [your-github-profile]  

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ for the Kenyan automotive industry**