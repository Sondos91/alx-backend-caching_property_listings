from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache
from django.utils import timezone
from .models import Property
import json


def test_cache(request):
    """Test view to verify Redis caching is working"""
    cache_key = 'test_cache_key'
    
    # Try to get from cache first
    cached_data = cache.get(cache_key)
    
    if cached_data is None:
        # If not in cache, create some data and cache it
        data = {
            'message': 'This data was fetched from the database and cached',
            'timestamp': timezone.now().isoformat(),
            'properties_count': Property.objects.count()
        }
        # Cache for 60 seconds
        cache.set(cache_key, data, 60)
        data['source'] = 'database'
    else:
        data = cached_data
        data['source'] = 'cache'
    
    return JsonResponse(data)


def property_list(request):
    """List all properties with caching"""
    cache_key = 'property_list_cache'
    
    # Try to get from cache first
    cached_properties = cache.get(cache_key)
    
    if cached_properties is None:
        # If not in cache, fetch from database
        properties = Property.objects.all().values('id', 'title', 'price', 'location', 'created_at')
        cached_properties = list(properties)
        # Cache for 300 seconds (5 minutes)
        cache.set(cache_key, cached_properties, 300)
        source = 'database'
    else:
        source = 'cache'
    
    return JsonResponse({
        'properties': cached_properties,
        'source': source,
        'count': len(cached_properties)
    })
