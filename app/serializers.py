import json
import django_rq

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.core.serializers import serialize
# from django.db.models import When, Case, Value, BooleanField

from app import models
from erp import models as erp_models
from app.tasks import create_check_task


# Item Serializer
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = (
            'id',
            'name',
            'quantity',
            'unit_price',
        )


# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    # items = ItemSerializer(many=True, write_only=True)
    id = serializers.IntegerField()
    price = serializers.IntegerField()

    class Meta:
        model = models.Order
        fields = (
            'id',
            'price',
            'items',
            'address',
            'client',
            'point_id',
        )

    def create(self, validated_data):
        check_id = validated_data['id']
        point_id = validated_data['point_id']
        items = validated_data['items']
        client = validated_data['client']
        price = validated_data['price']
        address = validated_data['address']

        if not erp_models.Printer.objects.printer_check(point_id):
            raise serializers.ValidationError(
                {'point_id': 'Недостаточно принтера'})

        items_json = json.loads(serialize('json', items))

        client_printer = erp_models.Printer.objects.filter(
            point_id=point_id, check_type=erp_models.CLIENT
        )
        kitchen_printer = erp_models.Printer.objects.filter(
            point_id=point_id, check_type=erp_models.KITCHEN
        )

        if erp_models.Check.objects.check_status(check_id):
            raise serializers.ValidationError(
                {'check_id': 'Квитанция уже выдана'})

        create_check = erp_models.Check.objects.bulk_create(
            [
                erp_models.Check(
                    order=items_json,
                    check_type=erp_models.CLIENT,
                    printer=client_printer.first(),
                    status=erp_models.NEW,
                    check_id=check_id,
                    address=address,
                    price=price,
                    name=client.name,
                    phone=client.phone,
                ),
                erp_models.Check(
                    order=items_json,
                    check_type=erp_models.KITCHEN,
                    printer=kitchen_printer.first(),
                    status=erp_models.NEW,
                    check_id=check_id,
                )
            ]
        )

        # queue = django_rq.get_queue('high')

        # queue.enqueue(
        #     generate_check, create_check[0].check_type, create_check[0]
        # )

        create_check_task.delay(
            create_check[0].check_type, create_check[0],
        )

        # generate_check(create_check[0].check_type, create_check[0])
        print('success rendered client check')

        create_check_task.delay(
            create_check[1].check_type, create_check[1],
        )
        print('success rendered kitchen check')

        return super().create(validated_data)


class CheckStatusNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = erp_models.Check
        fields = (
            'id',
            'check_id',
        )
