import datetime
from rest_framework import viewsets, mixins

from .tasks import write_location_data
from .models import Location, Device
from .serializers import LocationSerializer, DeviceSerializer, LocationListSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter


class LocationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    @extend_schema(
        responses={200: LocationSerializer(many=True)},
        description="Get device locations",
        methods=["GET"],
        parameters=[
            OpenApiParameter(
                name="start_date",
                location=OpenApiParameter.QUERY,
                description="Start date in format dd-mm-yyyy",
                required=False,
            ),
            OpenApiParameter(
                name="end_date",
                location=OpenApiParameter.QUERY,
                description="End date in format dd-mm-yyyy",
                required=False,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        queryset = Location.objects.all().order_by("-time")
        if start_date:
            try:
                start_date = datetime.datetime.strptime(start_date, "%d-%m-%Y")
                queryset = queryset.filter(time__gte=start_date)
            except ValueError:
                return Response(
                    {"error": "Invalid start_date format"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if end_date:
            try:
                end_date = datetime.datetime.strptime(end_date, "%d-%m-%Y")
                queryset = queryset.filter(time__lte=end_date)
            except ValueError:
                return Response(
                    {"error": "Invalid end_date format"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = LocationListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = LocationListSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = LocationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        write_location_data.delay(serializer.validated_data)
        return Response(status=201)


class DeviceViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = DeviceSerializer
    queryset = Device.objects.all()
    http_method_names = ["get", "post", "patch", "delete"]

    @extend_schema(
        responses={200: DeviceSerializer(many=True)},
        description="Get devices",
        methods=["GET"],
        parameters=[
            OpenApiParameter(
                name="status",
                location=OpenApiParameter.QUERY,
                description="Status of the device",
                required=False,
                type=str,
                enum=["active", "inactive"],
            ),
            OpenApiParameter(
                name="name",
                location=OpenApiParameter.QUERY,
                description="Name of the device",
                required=False,
                type=str,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        status = request.query_params.get("status")
        name = request.query_params.get("name")

        queryset = self.get_queryset()
        if status:
            queryset = queryset.filter(status=status)
        if name:
            queryset = queryset.filter(name__icontains=name)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        print("works")
        serializer = DeviceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        serializer.save()
        return Response(status=201)
