from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, BrowsableAPIRenderer
from drf_pdf.renderer import PDFRenderer
from drf_pdf.response import PDFResponse


from app import serializers, models
from erp import models as erp_models

# from app.utils import render_to_pdf
# Create your views here.


# Create Item
class ItemCreateView(generics.CreateAPIView):
    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer


# Create Check
class CheckCreateView(generics.CreateAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer


class CheckNewStatusRetreiveView(generics.GenericAPIView):
    queryset = erp_models.Check.objects.all()
    serializer_class = serializers.CheckStatusNewSerializer

    def get(self, request, *args, **kwargs):
        api_key = self.request.query_params.get('api_key')
        queryset = self.get_queryset()

        if not api_key:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not erp_models.Printer.objects.printer_api_key_check(api_key):
            return Response(
                {
                    "error": "Ошибка авторизации"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        res = {
            'checks': queryset.filter(
                Q(printer__api_key=api_key, status=erp_models.NEW) | Q(printer__api_key=api_key, status=erp_models.RENDERED)).values('check_id')
        }
        # serializers = self.get_serializer(queryset.filter(
        #     printer__api_key=api_key, status=erp_models.NEW), many=True)
        return Response(res, status=status.HTTP_200_OK)


class CheckPDFView(generics.GenericAPIView):
    queryset = erp_models.Check.objects.all()
    serializer_class = serializers.CheckStatusNewSerializer

    renderer_classes = (PDFRenderer, JSONRenderer,)

    def get(self, request, *args, **kwargs):
        api_key = self.request.query_params.get('api_key')
        check_id = self.request.query_params.get('check_id')

        if not api_key:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not check_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not erp_models.Printer.objects.printer_api_key_check(api_key):
            return Response(
                {
                    "error": "Ошибка авторизации"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not erp_models.Check.objects.check_status(check_id):
            return Response(
                {
                    "error": "Квитанция не найдена"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        check = erp_models.Check.objects.get(
            check_id=check_id, printer__api_key=api_key)

        return PDFResponse(
            pdf=check.pdf_file,
            file_name=check.pdf_file.url,
            status=status.HTTP_200_OK
        )
