import datetime
from .models import Location, Device
from rest_framework import serializers


class LocationSerializer(serializers.ModelSerializer):
    time = serializers.FloatField()
    device = serializers.UUIDField()

    class Meta:
        model = Location
        fields = ("device", "latitude", "longitude", "altitude", "speed", "time")

    def validate_time(self, value):
        if 0 > value > datetime.datetime.now().timestamp():
            raise serializers.ValidationError("Invalid timestamp")
        return value

    def validate_device(self, value):
        if not Device.objects.filter(id=value).exists():
            raise serializers.ValidationError("Device does not exist")
        return value

    def validate_latitude(self, value):
        if not -90 <= value <= 90:
            raise serializers.ValidationError("Latitude must be between -90 an 90")
        return value

    def validate_longitude(self, value):
        if not -180 <= value <= 180:
            raise serializers.ValidationError("Longitude must be between -180 an 180")
        return value

    def validate_speed(self, value):
        if value < 0:
            raise serializers.ValidationError("Speed must be positive")
        return value

    def validate_altitude(self, value):
        if value < 0:
            raise serializers.ValidationError("Altitude must be positive")
        return value


class LocationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("device", "latitude", "longitude", "altitude", "speed", "time")


class DeviceSerializer(serializers.ModelSerializer):
    last_location = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = ("id", "name", "type", "status", "last_location")

    def get_last_location(self, obj) -> LocationListSerializer:
        location = obj.locations.order_by("-time").first()
        if location:
            return LocationListSerializer(location).data  # type: ignore
        return {}  # type: ignore
