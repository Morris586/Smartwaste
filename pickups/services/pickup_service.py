


from .assignment import assign_truck_to_pickup


def handle_new_pickup(pickup):
    """
    Handles automatic truck assignment for a new pickup.
    """
    assign_truck_to_pickup(pickup)


def mark_pickup_collected(pickup):
    """
    Marks a pickup as collected and releases the driver.
    """

    if pickup.status != "assigned":
        return

    pickup.status = "collected"
    pickup.save()

    truck = pickup.assigned_truck

    if truck and truck.driver:
        truck.driver.status = "available"
        truck.driver.save()
