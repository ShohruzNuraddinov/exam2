from django.db import models

from utils.models import BaseModel

# Create your models here.


# client
class Client(BaseModel):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)


# item
class Item(BaseModel):
    name = models.CharField(max_length=128)
    quantity = models.IntegerField(default=0)
    unit_price = models.IntegerField(default=0)


# order
class Order(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, related_name='items')

    price = models.IntegerField(default=0)
    address = models.CharField(max_length=128)
    point_id = models.IntegerField()

