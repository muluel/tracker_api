from decimal import Decimal
from unittest.mock import patch
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from .tasks import write_location_data

from .models import Device, Location
from django.utils.timezone import now


class DeviceUnitTests(TestCase):
    def setUp(self):
        self.device = Device.objects.create(
            name="Test Device", type="type1", status="active"
        )

    def test_device_creation(self):
        self.assertEqual(self.device.name, "Test Device")
        self.assertEqual(self.device.type, "type1")
        self.assertEqual(self.device.status, "active")

    def tearDown(self):
        Device.objects.all().delete()


class LocationUnitTests(TestCase):
    def setUp(self):
        self.device = Device.objects.create(
            name="Test Device", type="type1", status="active"
        )
        self.location = Location.objects.create(
            device=self.device,
            latitude=41.0082,
            longitude=28.9784,
            altitude=123,
            speed=100,
            time=now(),
        )

    def test_location_creation(self):
        self.assertIsNotNone(self.location.id)

    def tearDown(self):
        Location.objects.all().delete()
        Device.objects.all().delete()


class LocationIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = APIRequestFactory()
        self.device = Device.objects.create(
            name="Test Device", type="type1", status="active"
        )
        self.location = Location.objects.create(
            device=self.device,
            latitude=41.0082,
            longitude=28.9784,
            altitude=123,
            speed=100,
            time=now(),
        )

    def test_location_list_endpoint(self):
        response = self.client.get(reverse("location-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)

    def test_location_create_endpoint(self):
        with patch("services.tasks.write_location_data.delay") as mock_task:
            data = {
                "device": self.device.pk,
                "latitude": Decimal("41.008200"),
                "longitude": Decimal("28.9784"),
                "altitude": Decimal("123"),
                "speed": Decimal("100"),
                "time": now().timestamp(),
            }
            response = self.client.post(
                reverse("location-list"), data=data, content_type="application/json"
            )
            self.assertEqual(response.status_code, 201)
            self.assertEqual(Location.objects.count(), 1)

            mock_task.assert_called_once_with(data)
            self.assertEqual(mock_task.call_count, 1)
            write_location_data(data)
            self.assertEqual(Location.objects.count(), 2)

    def tearDown(self):
        Location.objects.all().delete()
        Device.objects.all().delete()


class DeviceIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.device = Device.objects.create(
            name="Test Device", type="type1", status="active"
        )

    def test_device_list_endpoint(self):
        response = self.client.get(reverse("device-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)

    def test_device_create_endpoint(self):
        data = {"name": "New Device", "type": "type1", "status": "active"}
        response = self.client.post(
            reverse("device-list"), data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Device.objects.count(), 2)

    def tearDown(self):
        Device.objects.all().delete()
