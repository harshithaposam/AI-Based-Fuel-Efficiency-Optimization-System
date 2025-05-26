from django.core.cache import cache
from functools import wraps
import hashlib
import json

def cache_key_generator(*args, **kwargs):
    """Generate a cache key from the arguments"""
    key_parts = [str(arg) for arg in args]
    key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])
    key_string = "|".join(key_parts)
    return hashlib.md5(key_string.encode()).hexdigest()

def cache_response(timeout=300):
    """
    Cache decorator for view responses
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            # Generate cache key
            cache_key = f"view_{view_func.__name__}_{cache_key_generator(*args, **kwargs)}"
            
            # Try to get cached response
            response = cache.get(cache_key)
            if response is not None:
                return response
            
            # Generate response and cache it
            response = view_func(*args, **kwargs)
            cache.set(cache_key, response, timeout)
            return response
        return wrapped_view
    return decorator

def invalidate_route_cache(user_id):
    """Invalidate all route-related caches for a user"""
    cache_keys = [
        f'route_statistics_{user_id}',
        f'user_recommendations_{user_id}',
        f'recent_routes_{user_id}'
    ]
    cache.delete_many(cache_keys)