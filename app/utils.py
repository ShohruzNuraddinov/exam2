import pdfkit 
from django.template.loader import get_template

from erp import models as erp_models


def render_check(check_type, context={}):
    check_id = context['check_id']
    if check_type == erp_models.CLIENT:
        template = get_template('client_check.html')
    else:
        template = get_template('kitchen_check.html')

    html = template.render(context)

    pdf = pdfkit.from_string(html, f'media/checks/{check_id}_{check_type}.pdf')
    return f'checks/{check_id}_{check_type}.pdf'


def create_check(check_type, obj):

    if check_type == erp_models.CLIENT:
        context = {
            'check_id': obj.check_id,
            'name': obj.name,
            'phone': obj.phone,
            'addres': obj.address,
            'items': obj.order,
            'price': obj.price,
        }
    else:
        context = {
            'check_id': obj.check_id,
            'items': obj.order,
            'price': obj.price,
        }

    pdf_url = render_check(check_type, context)
    # obj.pdf_file.save(pdf_url, File(BytesIO(pdf_url)))
    obj.pdf_file = pdf_url
    obj.status = erp_models.RENDERED
    obj.save()
