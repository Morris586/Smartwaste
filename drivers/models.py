from django.db import models
from django.conf import settings
   
class Truck(models.Model):
    name = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20)
    capacity_tonnes = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    last_updated = models.DateTimeField(auto_now=True)

    driver = models.OneToOneField(
        'Driver',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='truck'
    )

    @property
    def is_available(self):
        """
        A truck is available if:
        - It has a driver
        - Driver status is 'available'
        - No active pickup (status='assigned')
        """

        if not self.driver:
            return False

        if self.driver.status != "available":
            return False

        active_pickup = self.pickups.filter(
            status="assigned"
        ).exists()

        return not active_pickup

    def __str__(self):
        return f"{self.name} ({self.license_plate})"

    

class Driver(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('en_route', 'En route'),
        ('off_duty', 'Off duty'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )

    def __str__(self):
        return self.name
