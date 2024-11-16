from django.db import models


class Device(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    status = models.CharField(
        max_length=100,
        default="inactive",
        choices=[("active", "Active"), ("inactive", "Inactive")],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Location(models.Model):
    time = TimescaleDateTimeField(interval="1 day")

    objects = TimescaleManager()
    timestamp = models.DateTimeField(primary_key=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()

    speed = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
