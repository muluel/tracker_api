from rest_framework import routers
from django.urls import path
from django.urls import include
from .views import DeviceViewset, LocationViewset

router = routers.DefaultRouter()
router.register(r"locations", LocationViewset)
router.register(r"devices", DeviceViewset)

urlpatterns = [
    path("", include(router.urls)),
]
