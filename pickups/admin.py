from django.contrib import admin
from .models import WastePickupRequest
from .services.pickup_service import handle_new_pickup
from drivers.models import Truck


@admin.register(WastePickupRequest)
class WastePickupRequestAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'phone',
        'waste_type',
        'address',
        'request_time',
        'status'
    )

    list_filter = ('waste_type', 'status')
    search_fields = ('name', 'phone', 'address')
    readonly_fields = ('longitude', 'latitude')

    fieldsets = (
        ("Client Info", {
            "fields": ('name', 'phone')
        }),
        ("Waste Information", {
            "fields": ('waste_type', 'address')
        }),
        ("Auto Coordinates", {
            "fields": ('latitude', 'longitude')
        }),
        ("Assignment", {
            "fields": ('assigned_truck',)
        }),
        ("Status Tracking", {
            "fields": ('status',)
        }),
    )

    def save_model(self, request, obj, form, change):
        previous_status = None

        if change:
            previous_obj = WastePickupRequest.objects.get(pk=obj.pk)
            previous_status = previous_obj.status

        super().save_model(request, obj, form, change)

        # When creating new pickup
        if not change:
            handle_new_pickup(obj)

        # When marking as collected
        if change and previous_status == "assigned" and obj.status == "collected":
            if obj.assigned_truck and obj.assigned_truck.driver:
                driver = obj.assigned_truck.driver
                driver.status = "available"
                driver.save()

def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == "assigned_truck":
        kwargs["queryset"] = Truck.objects.filter(is_available=True)
    return super().formfield_for_foreignkey(db_field, request, **kwargs)


