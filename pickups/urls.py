from django.urls import path

from. import views
from .views import request_pickup

urlpatterns = [ path("request/", request_pickup, name="request_pickup"),
               path("assigned/", views.assigned_pickups, name="assigned_pickups" ),
               path('collect/<int:pickup_id>/', views.mark_as_collected, name='mark_as_collected'),
               path("", views.pickups_home, name="pickups_home"),

]