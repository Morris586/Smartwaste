from django.contrib import admin
from .models import Driver, Truck

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'get_truck')
    search_fields = ('name', 'phone')

    def get_truck(self, obj):
        return obj.truck.name if hasattr(obj, 'truck') else None
    get_truck.short_description = 'Assigned Truck'

@admin.register(Truck)
class  TruckAdmin(admin.ModelAdmin):
    list_display = ('name', 'license_plate', 'capacity_tonnes', 'latitude', 'longitude','last_updated')
    search_fields = ('name', 'license_plate')



