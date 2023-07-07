from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from check_service.models import Printer, Check


class PrinterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Printer
        fields = "__all__"


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = "__all__"
        read_only_fields = ("id", "status", "pdf_file")



class CheckCreateSerializer(serializers.ModelSerializer):
    point_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Check
        fields = ("point_id", "type", "order")

        def create(self, validated_data):
            with transaction.atomic():
                type = validated_data["type"]
                order = validated_data["order"]
                point_id = validated_data["point_id"]
                printers = Printer.objects.filter(
                    point_id=point_id, check_type=type
                )

                if printers:
                    for printer in printers:
                        check = Check.objects.create(
                            printer_id=printer,
                            type=type,
                            order=order
                        )
                        create_pdf.delay(check.id)
                else:
                    raise ValidationError({"error":"printer for this check does not exist"})
                return point_id

        @staticmethod
        def representation():
            return "you have successfully created receipts for all printers"
