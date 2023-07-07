import base64
import json
import os.path

import requests
from celery import shared_task
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from SheepfishProject.settings import CHECK_CLIENT_TEMPLATE, CHECK_KITCHEN_TEMPLATE, WKHTMLTOPDF_URL, MEDIA_ROOT
from check_service.models import Check, Printer


def create_pdf_request(check: Check) -> Response:
    template = (
        CHECK_CLIENT_TEMPLATE
        if check.type == "Client"
        else CHECK_KITCHEN_TEMPLATE
    )
    check_html = render_to_string(template, {"check": check})
    b64_encode_html = base64.b64encode(bytes(check_html, "utf-8"))
    data = {
        "contents": b64_encode_html,
    }
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(
        WKHTMLTOPDF_URL, data=json.dumps(data), headers=headers
    )
    print(response)
    return response


@shared_task
def create_pdf(check_id: int) -> None:
    check = Check.objects.get(id == check_id)
    response = create_pdf_request(check)
    path_to_pdf = os.path.join("pdf", f"{check.id}_{check.type}.pdf")

    if os.path.exists(path_to_pdf):
        raise ValidationError(
            {f"Error": f"Pdf for check №{check.id} already exists"}
        )
    with open(os.path.join(MEDIA_ROOT, path_to_pdf), "wb") as file:
        file.write(response.content)
        check.pdf_file.name = path_to_pdf
        check.status = "rendered"
        check.save()


@shared_task
def create_pdf_for_all_checks_without_pdf() -> None:
    for check in Check.objects.filter(status="new"):
        create_pdf.delay(check.id)


@shared_task
def print_converted_checks() -> None:
    for printer in Printer.objects.all():
        for check in printer.checks.filter(status="rendered"):
            printer.print_check(check)
