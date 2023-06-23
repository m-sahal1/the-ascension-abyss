from django.db import models

# from .serializers import total_elevators, total_floors


class ElevatorSystem(models.Model):
    building_name = models.CharField(max_length=50)
    total_floors = models.PositiveIntegerField()
    total_elevators = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.building_name} : \n Floors: {self.total_floors} \n Elevators: {self.total_elevators}"


class Elevator(models.Model):
    STATUS_CHOICES = (
        ("idle", "Idle"),
        ("moving_up", "Moving Up"),
        ("moving_down", "Moving Down"),
    )
    DOOR_STATUS = (("open", "Door is Open"), ("close", "Door is Closed"))

    #the elevator id is primary key and django auto increments it and does not start it 
    # from 1 for each time a new system is initialised, so we use elevator_number for our needs 
    elevator_number = models.IntegerField()
    elevator_system=models.ForeignKey("ElevatorSystem", on_delete=models.CASCADE)
    operational = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="idle")
    current_floor = models.PositiveIntegerField(default=0)
    door = models.CharField(max_length=5, choices=DOOR_STATUS, default="close")

    def __str__(self):
        return f"Elevator {self.pk}"


class FloorRequest(models.Model):

    elevator = models.ForeignKey(Elevator, on_delete=models.CASCADE)
    requested_floor = models.PositiveSmallIntegerField()
    destination_floor = models.PositiveSmallIntegerField()
    request_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.elevator} is Requested: Floor {self.requested_floor}"
