from django.dispatch import receiver
from django.db.models.signals import post_save

from erp import models


@receiver(post_save, sender=models.Printer)
def printer_api_key(sender, instance, created, **kwargs):
    if created:
        instance.api_key = instance.generate_api_key()
        instance.save()


@receiver(post_save, sender=models.Check)
def render_check(sender, instance, created, **kwargs):
    if created:
        print(1)
