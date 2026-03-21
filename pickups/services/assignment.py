
# Distance-based assignment using Haversine formula

import math
from drivers.models import Truck
from django.db import transaction


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of earth in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))
    return R * c  # Distance in km


@transaction.atomic
def assign_truck_to_pickup(pickup):

    if pickup.status != "pending":
        return None

    candidate_trucks = Truck.objects.select_related("driver").all()


    nearest_truck = None
    shortest_distance = float("inf")

    for truck in candidate_trucks:

        if not truck.is_available:
            continue

        if None in [truck.latitude, truck.longitude, pickup.latitude, pickup.longitude]:
            continue

        distance = haversine_distance(
            pickup.latitude,
            pickup.longitude,
            truck.latitude,
            truck.longitude,
        )

        if distance < shortest_distance:
            shortest_distance = distance
            nearest_truck = truck

    if not nearest_truck:
        return None

    pickup.assigned_truck = nearest_truck
    pickup.status = "assigned"
    pickup.save()

    # update driver
    driver = nearest_truck.driver
    if driver:
        driver.status = "en_route"
        driver.save()

    return nearest_truck
