from django.urls import path
from . import views

urlpatterns = [
    path("", views.operations_dashboard, name='operations_dashboard'),
]