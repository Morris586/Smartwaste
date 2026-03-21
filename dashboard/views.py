from django.shortcuts import render
from pickups.models import WastePickupRequest
from drivers.models import Truck, Driver 
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def operations_dashboard(request):

    # Pickup metrics
    total_pickups = WastePickupRequest.objects.count()
    pending_pickups = WastePickupRequest.objects.filter(status="pending").count()
    assigned_pickups = WastePickupRequest.objects.filter(status="assigned").count()
    completed_pickups = WastePickupRequest.objects.filter(status="collected").count()

    # Driver metrics
    available_drivers = Driver.objects.filter(status="available").count()
    en_route_drivers = Driver.objects.filter(status="en_route").count()
    off_duty_drivers = Driver.objects.filter(status="off_duty").count()

    # Truck metrics
    total_trucks = Truck.objects.count()
    available_trucks = Truck.objects.filter(driver__status="available").count()
    busy_trucks = Truck.objects.filter(driver__status="en_route").count()

    # System health
    two_hours_ago = timezone.now() - timedelta(hours=2)
    stuck_pickups = WastePickupRequest.objects.filter(
        status="assigned",
        request_time__lt=two_hours_ago
    ).count()

    idle_dispatch = (
        WastePickupRequest.objects.filter(status="pending").exists()
        and Driver.objects.filter(status="available").exists()
    )

    context = {
        "total_pickups": total_pickups,
        "pending_pickups": pending_pickups,
        "assigned_pickups": assigned_pickups,
        "completed_pickups": completed_pickups,
        "available_drivers": available_drivers,
        "en_route_drivers": en_route_drivers,
        "off_duty_drivers": off_duty_drivers,
        "total_trucks": total_trucks,
        "available_trucks": available_trucks,
        "busy_trucks": busy_trucks,
        "stuck_pickups": stuck_pickups,
        "idle_dispatch": idle_dispatch
    }

    return render(request, "dashboard/dashboard.html", context)


def dashboard_home(request):
    # Simple function alias for operations_dashboard to satisfy imports
    return operations_dashboard(request)

