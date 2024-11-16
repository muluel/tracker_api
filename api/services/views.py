from rest_framework import viewsets

from .serializers import DeviceSerializer, LocationSerializer
from .models import Location, Device


class LocationViewset(viewsets.ModelViewSet):
    http_method_names = ["get", "post"]
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class DeviceViewset(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
