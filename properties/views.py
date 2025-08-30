from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache
from django.utils import timezone
from django.views.decorators.cache import cache_page
from .models import Property
from .utils import get_all_properties, get_redis_cache_metrics
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


@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    """List all properties with page-level caching"""
    properties = Property.objects.all().values('id', 'title', 'price', 'location', 'created_at')
    
    return JsonResponse({
        'properties': list(properties),
        'count': len(properties)
    })
