from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Property)
def invalidate_properties_cache_on_save(sender, instance, created, **kwargs):
    """
    Invalidate the all_properties cache when a Property is created or updated.
    """
    try:
        cache.delete('all_properties')
        action = "created" if created else "updated"
        logger.info(f"Property '{instance.title}' {action} - Cache 'all_properties' invalidated")
    except Exception as e:
        logger.error(f"Error invalidating cache on Property save: {str(e)}")


@receiver(post_delete, sender=Property)
def invalidate_properties_cache_on_delete(sender, instance, **kwargs):
    """
    Invalidate the all_properties cache when a Property is deleted.
    """
    try:
        cache.delete('all_properties')
        logger.info(f"Property '{instance.title}' deleted - Cache 'all_properties' invalidated")
    except Exception as e:
        logger.error(f"Error invalidating cache on Property delete: {str(e)}")
