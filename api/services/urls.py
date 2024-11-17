from rest_framework import routers
from .views import DeviceViewSet, LocationViewSet

router = routers.DefaultRouter()
router.register(r"locations", LocationViewSet)
router.register(r"devices", DeviceViewSet)
