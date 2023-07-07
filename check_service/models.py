from django.db import models


class TypeChoices(models.TextChoices):
    KITCHEN = 'kitchen', 'Kitchen'
    CLIENT = 'client', 'Client'


class StatusChoices(models.TextChoices):
    NEW = 'new', 'New'
    RENDERED = 'rendered', 'Rendered'
    PRINTED = 'printed', 'Printed'


class Printer(models.Model):
    name = models.CharField(max_length=67)
    api_key = models.CharField(max_length=67, unique=True, blank=True)
    check_type = models.CharField(max_length=67, choices=TypeChoices.choices)
    point_id = models.IntegerField()

    def save(self, *args, **kwargs):
        self.api_key = f"{self.point_id}_{self.check_type}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.api_key

    class Meta:
        unique_together = ("check_type", "point_id")


class Check(models.Model):
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE, related_name="checks")
    type = models.CharField(max_length=67, choices=TypeChoices.choices)
    order = models.JSONField()
    status = models.CharField(max_length=67, choices=StatusChoices.choices, default=StatusChoices.NEW)

    def __str__(self):
        order_id = self.order.get("id")
        return f"order_id_{order_id}_type{self.type}"

    class Meta:
        ordering = ("id",)
