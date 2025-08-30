from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property
import logging

logger = logging.getLogger(__name__)


def get_all_properties():
    """
    Get all properties with low-level Redis caching for 1 hour.
    Returns cached queryset if available, otherwise fetches from database.
    """
    # Check Redis for cached properties
    cached_properties = cache.get('all_properties')
    
    if cached_properties is None:
        # If not in cache, fetch from database
        properties = Property.objects.all()
        # Store in Redis for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)
        logger.info("Properties fetched from database and cached in Redis")
        return properties
    else:
        logger.info("Properties retrieved from Redis cache")
        return cached_properties


def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.
    Returns a dictionary with cache performance metrics.
    """
    try:
        # Get Redis connection via django_redis
        redis_conn = get_redis_connection("default")
        
        # Get Redis INFO command output
        info = redis_conn.info()
        
        # Extract keyspace hits and misses
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)
        
        # Calculate hit ratio
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = (keyspace_hits / total_requests * 100) if total_requests > 0 else 0
        
        # Get additional Redis metrics
        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_requests': total_requests,
            'hit_ratio_percentage': round(hit_ratio, 2),
            'hit_ratio_decimal': round(hit_ratio / 100, 4),
            'redis_version': info.get('redis_version', 'Unknown'),
            'connected_clients': info.get('connected_clients', 0),
            'used_memory_human': info.get('used_memory_human', 'Unknown'),
            'total_commands_processed': info.get('total_commands_processed', 0)
        }
        
        # Log the metrics
        logger.info(f"Redis Cache Metrics - Hit Ratio: {hit_ratio:.2f}%, "
                   f"Hits: {keyspace_hits}, Misses: {keyspace_misses}")
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {str(e)}")
        return {
            'error': str(e),
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'total_requests': 0,
            'hit_ratio_percentage': 0,
            'hit_ratio_decimal': 0
        }
