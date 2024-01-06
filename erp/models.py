import pdfkit

from django.db import models
from django.utils.crypto import get_random_string
from django.template.loader import get_template

from utils.models import BaseModel
from erp import managers

# Create your models here.
CLIENT = 'client'
KITCHEN = 'kitchen'

CHECK_TYPES = (
    ('client', CLIENT),
    ('kitchen', KITCHEN),
)

NEW = 'new'
RENDERED = 'rendered'
PRINTED = 'printed'

CHECK_STATUS = (
    ('new', NEW),
    ('rendered', RENDERED),
    ('printed', PRINTED),
)

# Printer


class Printer(BaseModel):
    name = models.CharField(max_length=128)
    api_key = models.CharField(max_length=128, blank=True, null=True)
    check_type = models.CharField(max_length=128, choices=CHECK_TYPES)
    point_id = models.IntegerField()

    objects = managers.PrinterManager()

    def generate_api_key(self):
        return get_random_string(length=32)


# Check
class Check(BaseModel):
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE, related_name='printers')  # noqa

    check_type = models.CharField(max_length=128, choices=CHECK_TYPES)
    order = models.JSONField()
    status = models.CharField(max_length=128, choices=CHECK_STATUS)
    pdf_file = models.FileField(upload_to='checks', blank=True, null=True)
    check_id = models.BigIntegerField()

    address = models.CharField(max_length=128, blank=True, null=True)
    price = models.IntegerField(default=0, blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=128, blank=True, null=True)

    objects = managers.CheckManager()

    def __str__(self) -> str:
        return str(self.id)
