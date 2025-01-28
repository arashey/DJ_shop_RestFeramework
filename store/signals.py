
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cart
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_cart_for_new_user(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance, is_paid=False)

