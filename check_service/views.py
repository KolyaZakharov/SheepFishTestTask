from rest_framework import viewsets

from check_service.models import Check, Printer
from check_service.serialiers import CheckSerializer, CheckCreateSerializer, PrinterSerializer


class CheckViewSet(viewsets.ModelViewSet):
    queryset = Check.objects.all()
    serializer_class = CheckSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return CheckCreateSerializer
        return CheckSerializer


class PrinterViewSet(viewsets.ModelViewSet):
    queryset = Printer.objects.all()
    serializer_class = PrinterSerializer
