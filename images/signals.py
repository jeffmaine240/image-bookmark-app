from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.text import slugify
from django.db import transaction

from .models import Image


@receiver(m2m_changed, sender=Image.users_like.through)
def m2m_changed_add_total_like(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        instance.total_likes = instance.users_like.count()
        if not instance.slug:
            instance.slug = slugify(instance.title)
        instance.save()

