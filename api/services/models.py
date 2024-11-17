from enum import Enum
from django.db import models
from timescale.db.models.fields import TimescaleDateTimeField
from timescale.db.models.managers import TimescaleManager
import uuid


class DeviceTypeEnum(Enum):
    TYPE1 = "type1"
    TYPE2 = "type2"

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]


class StatusEnum(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]


class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=100,
        choices=DeviceTypeEnum.choices(),
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=100, choices=StatusEnum.choices(), default=StatusEnum.INACTIVE.value
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.type})"


class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, related_name="locations"
    )
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    altitude = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    speed = models.DecimalField(max_digits=10, decimal_places=2)

    time = TimescaleDateTimeField(interval="1 day")
    objects = TimescaleManager()

    def __str__(self):
        return f"Location for {self.device.name} at {self.time}"
