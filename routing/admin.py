from django.contrib import admin

from .models import Route


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('truck', 'date', 'total_distance', 'total_duration')
    list_filter = ('date', 'truck')
    search_fields = ('truck__name',)

    filter_horizontal = ('pickups',)  # makes pickups field user-friendly