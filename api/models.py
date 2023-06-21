from django.db import models

# Create your models here.

class Elevator(models.Model):
    STATUS_CHOICES = (
        ('idle', 'Idle'),
        ('moving_up', 'Moving Up'),
        ('moving_down', 'Moving Down'),
        ('stopped', 'Stopped'),
    )
#add open close choices
# the elevator can be idle and open/close or it can be occupied and open/close
    operational = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='idle')
    current_floor = models.PositiveIntegerField(default=1)
    #destination floor
    #door open/close
    requests = models.ManyToManyField('FloorRequest', blank=True)

    def __str__(self):
        return f'Elevator {self.pk}'

class FloorRequest(models.Model):
    # DIRECTION_CHOICES = (
    #     ('up', 'Up'),
    #     ('down', 'Down'),
    # )

    floor = models.PositiveIntegerField() #the floor on which user is on
    # direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES)

    def __str__(self):
        return f'Request: Floor {self.floor} ({self.direction})'