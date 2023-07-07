import pytest
import responses
from django.test import RequestFactory
from check_service.utils import (
    create_pdf,
    create_pdf_request,
    create_pdf_for_all_checks_without_pdf,
    print_converted_checks,
)

from check_service.models import Check, Printer


@pytest.fixture
def check():
    return Check.objects.create(id=1, type="Client")


@pytest.fixture
def printer():
    return Printer.objects.create(name="Printer")


@responses.activate
def test_create_pdf_request(check):
    responses.add(responses.POST, 'http://example.com', status=200)

    response = create_pdf_request(check)

    assert response.status_code == 200


def test_create_pdf(check):
    factory = RequestFactory()
    request = factory.get('/')

    with responses.RequestsMock() as rsps:
        rsps.add(rsps.POST, 'http://example.com', status=200)

        create_pdf(request, check.id)

    check.refresh_from_db()
    assert check.status == "rendered"
    assert check.pdf_file.name is not None


def test_create_pdf_for_all_checks_without_pdf(check):
    create_pdf_for_all_checks_without_pdf()

    check.refresh_from_db()
    assert check.status == "rendered"
    assert check.pdf_file.name is not None


def test_print_converted_checks(check, printer):
    printer.checks.add(check)
    printer.print_check(check)

    print_converted_checks()

    check.refresh_from_db()
    assert check.status == "printed"
