from logging import Logger
from django.dispatch import Signal, receiver
from django.db.models.signals import post_save
from django.apps import apps

from .models import Order, Payment

@receiver(post_save, sender=Payment)
def trigger_order_is_paid_status(sender, instance, created, *args, **kwargs):
  if created:
    try:
      Order.objects.filter(id = instance.order.id).update(status=Order.RECEIVED)
      
    except Exception as err:
      print(err)