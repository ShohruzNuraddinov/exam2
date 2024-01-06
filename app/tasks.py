import logging

from django_rq import job

from app.utils import create_check
from erp import models as erp_models

logger = logging.getLogger(__name__)


@job
def create_check_task(check_type, obj):
    logger.info(f"{check_type} {obj}")
    create_check(check_type, obj)
    logger.info(f"Created check {check_type} {obj}")
