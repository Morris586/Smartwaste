from django.shortcuts import render, redirect, get_object_or_404
from .forms import WastePickupForm
from .services.assignment import assign_truck_to_pickup
from .models import WastePickupRequest
from .services.pickup_service import handle_new_pickup, mark_pickup_collected


def request_pickup(request):
    print("VIEW HIT")
    if request.method == 'POST':
        form=WastePickupForm(request.POST)
        if form.is_valid():
             pickup = form.save()
             handle_new_pickup(pickup)
            
             return redirect("home")
    else:
            form = WastePickupForm()
    return render(request, 'pickups/request_pickup.html', {'form': form})

def assigned_pickups(request):
    pickups=WastePickupRequest.objects.filter(status='assigned').select_related('assigned_truck')
    return render(request, "pickups/assigned_pickups.html", {'pickups': pickups})

def mark_as_collected(request, pickup_id):
     pickup = get_object_or_404(WastePickupRequest, id=pickup_id)
     mark_pickup_collected(pickup)

     return redirect('assigned_pickups')

def pickups_home(request):
     return render(request, 'pickups/home.html')


# Create your views here.
