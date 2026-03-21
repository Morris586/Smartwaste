from django.db import models
from django.conf import settings
from drivers.models import Truck


    
class Route(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    date = models.DateField()
    total_distance = models.FloatField()
    total_duration = models.FloatField()
    optimized_route = models.JSONField() # store route as a list of coordinates or waypoints
    pickups = models.ManyToManyField('pickups.WastePickupRequest')

    def __str__(self):
        return f"Route for {self.truck.name} on {self.date}"