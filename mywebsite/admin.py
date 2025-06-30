from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Brand, CarModel, Car, CarImage, Location, CarRental, 
    CustomerInquiry, BusinessConfig, Testimonial, BlogPost, 
    FAQ, CarComparison, NewsletterSubscription, ContactMessage
)

# Brand Admin
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'country_of_origin', 'created_at']
    list_filter = ['country_of_origin', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {}

# Car Model Admin
@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'body_type', 'created_at']
    list_filter = ['brand', 'body_type', 'created_at']
    search_fields = ['name', 'brand__name']

# Car Image Inline
class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1
    fields = ['image', 'caption', 'is_primary', 'order']

# Car Rental Inline
class CarRentalInline(admin.StackedInline):
    model = CarRental
    extra = 0
    fields = [
        ('daily_rate', 'weekly_rate', 'monthly_rate'),
        ('minimum_age', 'requires_license'),
        ('requires_deposit', 'deposit_amount'),
        ('max_rental_days', 'mileage_limit_per_day', 'extra_mileage_charge'),
        'rental_status',
        'terms_and_conditions'
    ]

# Car Admin
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = [
        'get_car_name', 'year', 'condition', 'price', 
        'status', 'location', 'views_count', 'is_featured'
    ]
    list_filter = [
        'condition', 'status', 'brand', 'fuel_type', 
        'transmission', 'location', 'is_featured', 'created_at'
    ]
    search_fields = ['brand__name', 'car_model__name', 'color']
    list_editable = ['price', 'status', 'is_featured']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('brand', 'car_model', 'year', 'condition', 'color')
        }),
        ('Technical Specifications', {
            'fields': ('engine_size', 'fuel_type', 'transmission', 'drive_type', 'mileage')
        }),
        ('Physical Specifications', {
            'fields': ('doors', 'seats')
        }),
        ('Pricing and Status', {
            'fields': ('price', 'negotiable', 'status')
        }),
        ('Location', {
            'fields': ('location',)
        }),
        ('Additional Information', {
            'fields': ('description', 'features', 'country_of_import', 'import_duty_paid')
        }),
        ('Marketing', {
            'fields': ('is_featured',)
        }),
        ('Metadata', {
            'fields': ('views_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    inlines = [CarImageInline, CarRentalInline]
    
    def get_car_name(self, obj):
        return f"{obj.year} {obj.brand.name} {obj.car_model.name}"
    get_car_name.short_description = 'Car'
    get_car_name.admin_order_field = 'brand__name'

# Location Admin
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'county', 'is_active']
    list_filter = ['county', 'is_active']
    search_fields = ['name', 'county']
    list_editable = ['is_active']

# Customer Inquiry Admin
@admin.register(CustomerInquiry)
class CustomerInquiryAdmin(admin.ModelAdmin):
    list_display = [
        'customer_name', 'customer_phone', 'inquiry_type', 
        'get_car_info', 'status', 'preferred_contact_method', 'created_at'
    ]
    list_filter = ['inquiry_type', 'status', 'preferred_contact_method', 'created_at']
    search_fields = ['customer_name', 'customer_phone', 'customer_email']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_phone', 'customer_email')
        }),
        ('Inquiry Details', {
            'fields': ('car', 'inquiry_type', 'message', 'preferred_contact_method')
        }),
        ('Management', {
            'fields': ('status', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_car_info(self, obj):
        if obj.car:
            return f"{obj.car.year} {obj.car.brand.name} {obj.car.car_model.name}"
        return "General Inquiry"
    get_car_info.short_description = 'Car'

# Business Config Admin
@admin.register(BusinessConfig)
class BusinessConfigAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'business_phone', 'business_email']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('business_name', 'business_phone', 'whatsapp_number', 'business_email', 'business_address')
        }),
        ('WhatsApp Integration', {
            'fields': ('whatsapp_message_template',)
        }),
        ('Business Hours', {
            'fields': ('opening_hours',)
        }),
        ('SEO Settings', {
            'fields': ('website_title', 'website_description', 'website_keywords')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url')
        })
    )

# Testimonial Admin
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'rating', 'is_featured', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_featured', 'is_approved', 'created_at']
    search_fields = ['customer_name', 'message']
    list_editable = ['is_featured', 'is_approved']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_location')
        }),
        ('Testimonial', {
            'fields': ('message', 'rating', 'car_purchased')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_approved')
        })
    )

# Blog Post Admin
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'published_at', 'views_count']
    list_filter = ['is_published', 'published_at', 'author']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published']
    readonly_fields = ['views_count']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'featured_image')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Publication', {
            'fields': ('author', 'is_published', 'published_at')
        }),
        ('Statistics', {
            'fields': ('views_count',)
        })
    )

# FAQ Admin
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['question', 'answer']
    list_editable = ['order', 'is_active']

# Newsletter Subscription Admin
@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    list_editable = ['is_active']

# Contact Message Admin
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Management', {
            'fields': ('is_read', 'created_at')
        })
    )

# Car Comparison Admin
@admin.register(CarComparison)
class CarComparisonAdmin(admin.ModelAdmin):
    list_display = ['get_comparison_info', 'user', 'created_at']
    list_filter = ['created_at']
    readonly_fields = ['created_at']
    
    def get_comparison_info(self, obj):
        cars = obj.cars.all()
        if cars:
            return f"Comparison of {cars.count()} cars"
        return "Empty comparison"
    get_comparison_info.short_description = 'Comparison'

# Customize Admin Site
admin.site.site_header = "Car Dealership Admin"
admin.site.site_title = "Car Dealership Admin Portal"
admin.site.index_title = "Welcome to Car Dealership Administration"