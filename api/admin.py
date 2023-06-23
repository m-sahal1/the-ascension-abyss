from django.contrib import admin
from .models import Elevator, FloorRequest, ElevatorSystem
# Register your models here.

admin.site.register(Elevator)
admin.site.register(FloorRequest)
admin.site.register(ElevatorSystem)
