from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    # Homepage
    path('', views.homepage, name='homepage'),
    path('cars/<slug:slug>/', views.car_detail, name='car_detail'),
    
    # AJAX endpoints
    path('ajax/models-by-brand/', views.get_models_by_brand, name='models_by_brand'),
    path('ajax/car-detail/<int:car_id>/', views.car_detail_ajax, name='car_detail_ajax'),
    path('ajax/submit-inquiry/', views.submit_inquiry, name='submit_inquiry'),
    path('ajax/newsletter-subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
]