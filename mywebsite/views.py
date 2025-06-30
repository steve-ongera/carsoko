from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Count, Min, Max
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .models import (
    Car, Brand, CarModel, Location, CarImage, CarRental, 
    CustomerInquiry, BusinessConfig, Testimonial, BlogPost, FAQ
)

def homepage(request):
    """
    Homepage view that displays car listings, search functionality,
    and business information for the car dealership.
    """
    
    # Get business configuration
    try:
        business_config = BusinessConfig.objects.first()
    except BusinessConfig.DoesNotExist:
        business_config = None
    
    # Get available cars for display
    available_cars = Car.objects.filter(
        status='available'
    ).select_related(
        'brand', 'car_model', 'location'
    ).prefetch_related('images')
    
    # Get featured cars (limit to 8 for homepage display)
    featured_cars = available_cars.filter(is_featured=True)[:8]
    
    # If not enough featured cars, fill with recent cars
    if featured_cars.count() < 8:
        additional_cars = available_cars.exclude(
            id__in=[car.id for car in featured_cars]
        ).order_by('-created_at')[:8 - featured_cars.count()]
        
        # Combine featured and additional cars
        homepage_cars = list(featured_cars) + list(additional_cars)
    else:
        homepage_cars = featured_cars
    
    # Separate cars for sale and rent
    cars_for_sale = []
    cars_for_rent = []
    
    for car in homepage_cars:
        # Check if car has rental info
        if hasattr(car, 'rental_info'):
            cars_for_rent.append(car)
        else:
            cars_for_sale.append(car)
    
    # Get filter options for search forms
    # Years (from cars in database)
    years = Car.objects.values_list('year', flat=True).distinct().order_by('-year')
    
    brands = Brand.objects.filter(
        car__status='available'
    ).distinct().order_by('name')
    
    # Get popular models (with car count)
    popular_models = CarModel.objects.filter(
        car__status='available'
    ).annotate(
        car_count=Count('car')
    ).order_by('-car_count')[:10]
    
    # Price range for available cars
    price_range = Car.objects.filter(status='available').aggregate(
        min_price=Min('price'),
        max_price=Max('price')
    )
    
    # Get locations with available cars
    locations = Location.objects.filter(
        car__status='available',
        is_active=True
    ).distinct().order_by('county', 'name')
    
    # Get testimonials for homepage
    testimonials = Testimonial.objects.filter(
        is_approved=True,
        is_featured=True
    ).order_by('-created_at')[:3]
    
    # Get latest blog posts
    latest_posts = BlogPost.objects.filter(
        is_published=True,
        published_at__lte=timezone.now()
    ).order_by('-published_at')[:3]
    
    # Car statistics for display
    car_stats = {
        'total_cars': available_cars.count(),
        'cars_for_sale': Car.objects.filter(status='available').exclude(rental_info__isnull=False).count(),
        'cars_for_rent': Car.objects.filter(status='available', rental_info__isnull=False).count(),
        'total_brands': brands.count(),
    }
    
    # Process search if GET parameters are present
    search_results = None
    if request.GET.get('search'):
        search_results = process_car_search(request)
    
    context = {
        'business_config': business_config,
        'homepage_cars': homepage_cars,
        'cars_for_sale': cars_for_sale,
        'cars_for_rent': cars_for_rent,
        'years': years,
        'brands': brands,
        'popular_models': popular_models,
        'locations': locations,
        'price_range': price_range,
        'testimonials': testimonials,
        'latest_posts': latest_posts,
        'car_stats': car_stats,
        'search_results': search_results,
    }
    
    return render(request, 'homepage.html', context)


def process_car_search(request):
    """
    Process car search based on form parameters
    """
    cars = Car.objects.filter(status='available').select_related(
        'brand', 'car_model', 'location'
    ).prefetch_related('images')
    
    # Filter by year
    year = request.GET.get('year')
    if year:
        cars = cars.filter(year=year)
    
    # Filter by brand
    brand_id = request.GET.get('brand')
    if brand_id:
        cars = cars.filter(brand_id=brand_id)
    
    # Filter by model
    model_id = request.GET.get('model')
    if model_id:
        cars = cars.filter(car_model_id=model_id)
    
    # Filter by mileage (assuming it's maximum mileage in thousands)
    mileage = request.GET.get('mileage')
    if mileage:
        try:
            max_mileage = int(mileage) * 1000  # Convert to actual mileage
            cars = cars.filter(mileage__lte=max_mileage)
        except ValueError:
            pass
    
    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if min_price:
        try:
            cars = cars.filter(price__gte=float(min_price))
        except ValueError:
            pass
    
    if max_price:
        try:
            cars = cars.filter(price__lte=float(max_price))
        except ValueError:
            pass
    
    # Filter by location
    location_id = request.GET.get('location')
    if location_id:
        cars = cars.filter(location_id=location_id)
    
    # Filter by fuel type
    fuel_type = request.GET.get('fuel_type')
    if fuel_type:
        cars = cars.filter(fuel_type=fuel_type)
    
    # Filter by transmission
    transmission = request.GET.get('transmission')
    if transmission:
        cars = cars.filter(transmission=transmission)
    
    # Search by keyword (searches in brand name, model name, and description)
    keyword = request.GET.get('keyword')
    if keyword:
        cars = cars.filter(
            Q(brand__name__icontains=keyword) |
            Q(car_model__name__icontains=keyword) |
            Q(description__icontains=keyword) |
            Q(features__icontains=keyword)
        )
    
    # Filter by car type (rental or sale)
    car_type = request.GET.get('car_type')
    if car_type == 'rental':
        cars = cars.filter(rental_info__isnull=False)
    elif car_type == 'sale':
        cars = cars.filter(rental_info__isnull=True)
    
    return cars.order_by('-created_at')


def get_models_by_brand(request):
    """
    AJAX view to get car models based on selected brand
    """
    brand_id = request.GET.get('brand_id')
    models = []
    
    if brand_id:
        models = list(
            CarModel.objects.filter(brand_id=brand_id).values('id', 'name')
        )
    
    return JsonResponse({'models': models})


def car_detail_ajax(request, car_id):
    """
    AJAX view to get car details for quick view modals
    """
    try:
        car = Car.objects.select_related(
            'brand', 'car_model', 'location'
        ).prefetch_related('images').get(id=car_id, status='available')
        
        # Increment view count
        car.increment_views()
        
        # Get primary image
        primary_image = car.images.filter(is_primary=True).first()
        all_images = car.images.all().order_by('order', 'uploaded_at')
        
        # Check if car has rental info
        rental_info = None
        if hasattr(car, 'rental_info'):
            rental_info = {
                'daily_rate': float(car.rental_info.daily_rate),
                'weekly_rate': float(car.rental_info.weekly_rate) if car.rental_info.weekly_rate else None,
                'monthly_rate': float(car.rental_info.monthly_rate) if car.rental_info.monthly_rate else None,
                'minimum_age': car.rental_info.minimum_age,
                'requires_deposit': car.rental_info.requires_deposit,
                'deposit_amount': float(car.rental_info.deposit_amount) if car.rental_info.deposit_amount else None,
            }
        
        car_data = {
            'id': car.id,
            'brand': car.brand.name,
            'model': car.car_model.name,
            'year': car.year,
            'price': float(car.price),
            'condition': car.get_condition_display(),
            'fuel_type': car.get_fuel_type_display(),
            'transmission': car.get_transmission_display(),
            'mileage': car.mileage,
            'color': car.color,
            'doors': car.doors,
            'seats': car.seats,
            'location': str(car.location),
            'description': car.description,
            'features': car.features.split(',') if car.features else [],
            'negotiable': car.negotiable,
            'primary_image': primary_image.image.url if primary_image else None,
            'all_images': [img.image.url for img in all_images],
            'rental_info': rental_info,
            'is_rental': rental_info is not None,
        }
        
        return JsonResponse({'success': True, 'car': car_data})
        
    except Car.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Car not found'})


def submit_inquiry(request):
    """
    Handle customer inquiry form submission
    """
    if request.method == 'POST':
        try:
            # Get form data
            car_id = request.POST.get('car_id')
            inquiry_type = request.POST.get('inquiry_type', 'general')
            customer_name = request.POST.get('customer_name')
            customer_phone = request.POST.get('customer_phone')
            customer_email = request.POST.get('customer_email', '')
            message = request.POST.get('message')
            preferred_contact = request.POST.get('preferred_contact', 'whatsapp')
            
            # Validate required fields
            if not all([customer_name, customer_phone, message]):
                return JsonResponse({
                    'success': False, 
                    'error': 'Please fill in all required fields'
                })
            
            # Get car if specified
            car = None
            if car_id:
                try:
                    car = Car.objects.get(id=car_id)
                except Car.DoesNotExist:
                    pass
            
            # Create inquiry
            inquiry = CustomerInquiry.objects.create(
                car=car,
                inquiry_type=inquiry_type,
                customer_name=customer_name,
                customer_phone=customer_phone,
                customer_email=customer_email,
                message=message,
                preferred_contact_method=preferred_contact,
            )
            
            # Generate WhatsApp message if business config exists
            whatsapp_url = None
            try:
                business_config = BusinessConfig.objects.first()
                if business_config and car:
                    template = business_config.whatsapp_message_template
                    whatsapp_message = template.format(
                        car_year=car.year,
                        car_brand=car.brand.name,
                        car_model=car.car_model.name,
                        car_price=f"KES {car.price:,.0f}"
                    )
                    whatsapp_number = business_config.whatsapp_number.replace('+', '').replace(' ', '')
                    whatsapp_url = f"https://wa.me/{whatsapp_number}?text={whatsapp_message}"
            except:
                pass
            
            response_data = {
                'success': True,
                'message': 'Thank you for your inquiry! We will contact you soon.',
                'inquiry_id': inquiry.id
            }
            
            if whatsapp_url:
                response_data['whatsapp_url'] = whatsapp_url
            
            return JsonResponse(response_data)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': 'An error occurred while submitting your inquiry. Please try again.'
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def newsletter_subscribe(request):
    """
    Handle newsletter subscription
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if not email:
            return JsonResponse({'success': False, 'error': 'Email is required'})
        
        try:
            from .models import NewsletterSubscription
            subscription, created = NewsletterSubscription.objects.get_or_create(
                email=email,
                defaults={'is_active': True}
            )
            
            if created:
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you for subscribing to our newsletter!'
                })
            else:
                if subscription.is_active:
                    return JsonResponse({
                        'success': False,
                        'error': 'This email is already subscribed'
                    })
                else:
                    # Reactivate subscription
                    subscription.is_active = True
                    subscription.save()
                    return JsonResponse({
                        'success': True,
                        'message': 'Welcome back! Your subscription has been reactivated.'
                    })
                    
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': 'An error occurred. Please try again.'
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


# Additional utility functions

def get_car_features_list(car):
    """
    Helper function to get formatted car features list
    """
    if not car.features:
        return []
    
    features = [feature.strip() for feature in car.features.split(',')]
    return [feature for feature in features if feature]


def format_price_range(min_price, max_price):
    """
    Helper function to format price range for display
    """
    if min_price and max_price:
        return f"KES {min_price:,.0f} - KES {max_price:,.0f}"
    elif min_price:
        return f"From KES {min_price:,.0f}"
    elif max_price:
        return f"Up to KES {max_price:,.0f}"
    return "Price on request"


def get_whatsapp_url(car, business_config=None):
    """
    Generate WhatsApp URL for car inquiry
    """
    if not business_config:
        try:
            business_config = BusinessConfig.objects.first()
        except BusinessConfig.DoesNotExist:
            return None
    
    if not business_config:
        return None
    
    try:
        template = business_config.whatsapp_message_template
        message = template.format(
            car_year=car.year,
            car_brand=car.brand.name,
            car_model=car.car_model.name,
            car_price=f"KES {car.price:,.0f}"
        )
        
        whatsapp_number = business_config.whatsapp_number.replace('+', '').replace(' ', '')
        return f"https://wa.me/{whatsapp_number}?text={message}"
    except:
        return None