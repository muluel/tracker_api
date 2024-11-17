from celery import shared_task
from datetime import datetime, timezone

from services.models import Location


@shared_task
def write_location_data(data):
    time = datetime.fromtimestamp(data["time"]).astimezone(timezone.utc)
    Location.objects.create(
        device_id=data["device"],
        latitude=data["latitude"],
        longitude=data["longitude"],
        altitude=data.get("altitude"),
        speed=data["speed"],
        time=time,
    )
    return True
