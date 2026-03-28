import math
import logging
from drivers.models import Truck
from django.db import transaction

logger = logging.getLogger(__name__)

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))
    return R * c


@transaction.atomic
def assign_truck_to_pickup(pickup):
    logger.info(f"[ASSIGN] Called for pickup ID={pickup.id}, status={pickup.status}")

    if pickup.status != "pending":
        logger.warning(f"[ASSIGN] Pickup {pickup.id} skipped — status is '{pickup.status}', expected 'pending'")
        return None

    candidate_trucks = Truck.objects.select_related("driver").all()
    logger.info(f"[ASSIGN] Total trucks in DB: {candidate_trucks.count()}")

    nearest_truck = None
    shortest_distance = float("inf")

    for truck in candidate_trucks:
        if not truck.is_available:
            logger.info(f"[ASSIGN] Truck {truck.id} skipped — not available")
            continue

        if None in [truck.latitude, truck.longitude, pickup.latitude, pickup.longitude]:
            logger.info(f"[ASSIGN] Truck {truck.id} skipped — missing coordinates. "
                        f"truck=({truck.latitude},{truck.longitude}), "
                        f"pickup=({pickup.latitude},{pickup.longitude})")
            continue

        distance = haversine_distance(
            pickup.latitude, pickup.longitude,
            truck.latitude, truck.longitude,
        )
        logger.info(f"[ASSIGN] Truck {truck.id} is {distance:.2f} km away")

        if distance < shortest_distance:
            shortest_distance = distance
            nearest_truck = truck

    if not nearest_truck:
        logger.warning(f"[ASSIGN] No suitable truck found for pickup {pickup.id}")
        return None

    pickup.assigned_truck = nearest_truck
    pickup.status = "assigned"
    pickup.save()

    driver = nearest_truck.driver
    if driver:
        driver.status = "en_route"
        driver.save()

    logger.info(f"[ASSIGN] Pickup {pickup.id} assigned to truck {nearest_truck.id}")
    return nearest_truck


