from django.urls import path, include
from rest_framework import routers

from check_service.views import PrinterViewSet, CheckViewSet

router = routers.DefaultRouter()
router.register("printers", PrinterViewSet)
router.register("checks", CheckViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "check"
