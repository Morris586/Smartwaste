from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import WastePickupRequest

@receiver(post_save, sender=WastePickupRequest)
def release_truck_on_completion(sender, instance, **kwargs):#if pickup is marked as completed release th truck

    if instance.status == ['collected', 'completed'] and instance.assigned_truck:
        truck=instance.assigned_truck
        if not truck.is_available:
            truck.is_available = True
            truck.save() 
            print(f"Truck {truck.name} released to the available pool")
