from django.db import models
import openrouteservice
from django.conf import settings

class WastePickupRequest(models.Model):
    WASTE_TYPES = [
        ('organic', 'Organic'),
        ('plastic', 'Plastic'),
        ('e-waste', 'E-waste'),
        ('mixed', 'Mixed'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('collected', 'Collected'),
        ('completed', 'Completed'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    waste_type = models.CharField(max_length=20, choices=WASTE_TYPES)
    address = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    assigned_truck = models.ForeignKey(
        'drivers.Truck',  null=True, blank=True, on_delete=models.SET_NULL, related_name='pickups' )#assigned truck for pickup
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')#status lifecycle 

    request_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.waste_type}"

    def save(self, *args, **kwargs):
        from pickups.services.pickup_service import handle_new_pickup

        is_new = self.pk is None  # Check if this is first save

        # Auto-generate coordinates if not provided
        if (self.latitude is None or self.longitude is None) and self.address:
            try:
                client = openrouteservice.Client(key=settings.ORS_API_KEY)
                response = client.pelias_search(text=self.address)

                if response and response['features']:
                    coords = response['features'][0]['geometry']['coordinates']
                    self.longitude = coords[0]
                    self.latitude = coords[1]
            except Exception as e:
                print("Geocoding error:", e)

        super().save(*args, **kwargs)

        # Trigger assignment only on creation and only if still pending
        if is_new and self.status == "pending":
            handle_new_pickup(self)

    def delete(self, *args, **kwargs):
        # If pickup is deleted, release the truck and driver
        if self.assigned_truck and self.assigned_truck.driver:
            self.assigned_truck.driver.status = "available"
            self.assigned_truck.driver.save()
        super().delete(*args, **kwargs)

