from django.db import models

from erp import models as erp_models


class PrinterManager(models.Manager):
    def printer_check(self, point_id) -> bool:

        if self.get_queryset().filter(
           point_id=point_id, check_type=erp_models.CLIENT).exists() and \
            self.get_queryset().filter(
                point_id=point_id, check_type=erp_models.KITCHEN
        ).exists():
            return True
        return False

    def printer_api_key_check(self, api_key) -> bool:
        if self.get_queryset().filter(api_key=api_key).exists():
            return True
        return False


class CheckManager(models.Manager):
    def check_status(self, check_id) -> bool:
        if self.get_queryset().filter(
            check_id=check_id, check_type=erp_models.CLIENT
        ).exists() and \
            self.get_queryset().filter(
            check_id=check_id, check_type=erp_models.KITCHEN
        ):
            return True
        return False
